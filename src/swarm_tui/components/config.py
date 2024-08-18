from __future__ import annotations

import json

from rich.pretty import Pretty
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import TabbedContent, TabPane, TextArea

from ..exceptions import DockerApiError
from .datatable_nav import DataTableNav
from .info_panel import InfoPanel
from .models import SelectedContent
from .navigable_panel import NavigablePanel


class Config(NavigablePanel):
    BORDER_TITLE = "Config"

    BINDINGS = [
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("r", "rename", "Rename"),
    ]

    data: reactive[list[str]] = reactive([])

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="config-dt", filter_field="Name")
        self.table.cursor_type = "none"
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        for row in range(2):
            self.table.add_row(f"Config {row}", key=f"Config {row}")
        self.table.move_cursor()
        yield self.table

    def watch_data(self, rows: list[str]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(row, key=row)
        self.table.sort("Name", key=lambda x: x.lower())


class ConfigInfo(InfoPanel):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        self.info = TextArea(read_only=True, language="json")
        self.config = TextArea(read_only=True)
        with TabbedContent():
            with TabPane("Info", id="info"):
                yield self.info
            with TabPane("Config", id="config"):
                yield self.config

    async def watch_selected(self, selected: SelectedContent) -> None:
        if not selected:
            return
        tc = self.query_one(TabbedContent)
        tc.border_title = f"Config: {selected.selected_id}"
        tc.active = "info"
        await self.update_active_tab(selected.selected_id, tc.active)

    async def on_tabbed_content_tab_activated(
        self, message: TabbedContent.TabActivated
    ):
        if not self.selected:
            return

        await self.update_active_tab(
            self.selected.selected_id, message.tabbed_content.active
        )

    async def update_active_tab(self, selected_id: str, tab_id: str) -> None:
        component = self.info if tab_id == "info" else self.config
        try:
            info = await self.backend.get_config_info(selected_id)
            if tab_id == "info":
                component.text = json.dumps(info, indent=2, sort_keys=True)
            else:
                data = await self.backend.decode_config_data(info["Spec"]["Data"])
                component.text = data
        except DockerApiError as e:
            self.notify(str(e), severity="error")
            component.text = "{}"
