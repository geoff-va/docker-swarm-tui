from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, Static, TabbedContent, TextArea

from .datatable_nav import DataTableNav
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


class ConfigInfo(Static):
    BORDER_TITLE = "Config Info"

    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Info", "Config") as tc:
            tc.border_title = "Config Info"
            yield TextArea("Info")
            yield Pretty({"key": "value"})
