from __future__ import annotations

import json

from textual import work
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import TabbedContent, TextArea

from ..exceptions import DockerApiError
from .datatable_nav import DataTableNav
from .info_panel import InfoPanel
from .models import SelectedContent
from .navigable_panel import NavigablePanel


class Secrets(NavigablePanel):
    BORDER_TITLE = "Secrets"

    BINDINGS = [
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("r", "rename", "Rename"),
    ]

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="secrets-dt", filter_field="Name")
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        yield self.table

    def focus_child(self) -> None:
        self.table.focus()

    async def action_delete(self) -> None:
        if not self.table.is_valid_coordinate(self.table.cursor_coordinate):
            return

        cell = self.table.coordinate_to_cell_key(self.table.cursor_coordinate)
        try:
            await self.backend.remove_secret(cell.row_key.value)
            self.notify(f"Removed Secret: {cell.row_key.value}", title="Secrets")
            await self.reload_table()
        except DockerApiError as e:
            self.notify(str(e), title="Secrets", severity="error")

    async def reload_table(self) -> None:
        rows = await self.backend.get_secrets()
        self.table.clear()
        for row in rows:
            self.table.add_row(row, key=row)
        self.table.sort("Name", key=lambda x: x.lower())


class SecretsInfo(InfoPanel):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        self.component = TextArea(read_only=True, language="json")
        with TabbedContent("Info"):
            yield self.component

    async def watch_selected(self, selected: SelectedContent) -> None:
        if selected is None:
            return
        try:
            self.query_one(
                TabbedContent
            ).border_title = f"Secret: {selected.selected_id}"
            info = await self.backend.get_secret_info(selected.selected_id)
            self.component.text = json.dumps(info, indent=2, sort_keys=True)
        except DockerApiError as e:
            self.notify(str(e), severity="error")
            self.component.text = "{}"
