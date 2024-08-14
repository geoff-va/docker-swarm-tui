from textual.app import ComposeResult
from textual.widgets import Static

from .datatable_nav import DataTableNav


class Secrets(Static):
    BORDER_TITLE = "Secrets"

    BINDINGS = [
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("r", "rename", "Rename"),
    ]

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="secrets-dt", filter_field="Name")
        self.table.cursor_type = "row"
        self.table.add_column("Name", key="Name")
        self.table.add_rows([["Secret 1"], ["Secret 2"]])
        yield self.table
