from textual.app import ComposeResult
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

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="secrets-dt", filter_field="Name")
        self.table.add_column("Name", key="Name")
        self.table.add_row("secret 1", key="secret 1")
        self.table.add_row("secret 2", key="secret 2")
        yield self.table


class SecretsInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Secrets Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Secret": "Content"})
