from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, TabbedContent

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
        self.component = Pretty({})
        with TabbedContent("Info"):
            yield self.component

    async def watch_selected(self, selected: SelectedContent) -> None:
        if not selected:
            return
        self.query_one(TabbedContent).border_title = f"Config: {selected.selected_id}"
        info = await self.backend.get_config_info(selected.selected_id)
        self.component.update(info)
