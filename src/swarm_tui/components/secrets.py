from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, Static, TabbedContent

from .datatable_nav import DataTableNav, SelectionChanged
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
        self.table.add_column("Name", key="Name")
        yield self.table

    def watch_data(self, secrets: list[str]) -> None:
        self.table.clear()
        for secret in secrets:
            self.table.add_row(secret, key=secret)
        self.table.sort("Name", key=lambda x: x.lower())


class SecretsInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Secrets Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Secret": "Content"})
