from __future__ import annotations

import json

from aiodocker import Docker
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

    data: reactive[list[str]] = reactive([])

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="secrets-dt", filter_field="Name")
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        yield self.table

    def focus_child(self) -> None:
        self.table.focus()

    def watch_data(self, rows: list[str]) -> None:
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
        if not selected:
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
