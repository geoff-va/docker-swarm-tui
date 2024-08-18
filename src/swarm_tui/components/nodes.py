from __future__ import annotations

import json

from textual.app import ComposeResult
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
        ("w", "worker", "Worker Token"),
        ("m", "manager", "Manger Token"),
    ]

    data: reactive[list[Node]] = reactive([])

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="nodes-dt", filter_field="Name")
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        yield self.table

    def watch_data(self, rows: list[Node]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(row.hostname, key=row.id)
        self.table.sort("Name", key=lambda x: x.lower())


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
