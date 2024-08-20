from __future__ import annotations

import json

from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import TabbedContent, TextArea

from ..backends.models import Node
from ..exceptions import DockerApiError
from .datatable_nav import DataTableNav
from .info_panel import InfoPanel
from .models import SelectedContent
from .navigable_panel import NavigablePanel


class Nodes(NavigablePanel):
    BORDER_TITLE = "Nodes"

    BINDINGS = [
        # TODO: Implement these
        # Binding("d", "demote", "Demote"),
        # Binding("p", "promote", "Promote"),
        Binding("r", "remove", "Remove"),
        Binding("R", "force_remove", "Force Remove"),
    ]

    data: reactive[list[Node]] = reactive([])

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="nodes-dt", filter_field="Name")
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        yield self.table

    def focus_child(self) -> None:
        self.table.focus()

    def watch_data(self, rows: list[Node]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(row.hostname, key=row.id)
        self.table.sort("Name", key=lambda x: x.lower())

    async def action_remove(self) -> None:
        try:
            await self.remove_highlighted_node(force=False)
        except DockerApiError as e:
            self.notify(str(e), title="Remove Node Failed", severity="error")

    async def action_force_remove(self) -> None:
        try:
            await self.remove_highlighted_node(force=True)
        except DockerApiError as e:
            self.notify(str(e), title="Remove Node (force) Failed", severity="error")

    async def remove_highlighted_node(self, force: bool = False) -> None:
        # TODO: will need to refresh nodes or monitor events looking for node removal
        cell = self.table.coordinate_to_cell_key(self.table.cursor_coordinate)
        assert cell.row_key.value
        node_id = cell.row_key.value
        hostname = self.table.get_cell_at(self.table.cursor_coordinate)
        await self.backend.remove_node(node_id, force=force)
        title = "Node Removed (force)" if force else "Node Removed"
        self.notify(
            message=f"Removed: {hostname} ({node_id})",
            title=title,
            severity="information",
        )


class NodeInfo(InfoPanel):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        self.component = TextArea(read_only=True, language="json")
        with TabbedContent("Info"):
            yield self.component

    async def watch_selected(self, selected: SelectedContent) -> None:
        if not selected:
            return
        self.query_one(TabbedContent).border_title = f"Node: {selected.selected_id}"
        try:
            info = await self.backend.get_node_info(selected.selected_id)
            self.component.text = json.dumps(info, indent=2, sort_keys=True)
        except DockerApiError as e:
            self.notify(str(e), severity="error")
            self.component.text = "{}"
