from textual.app import ComposeResult
from textual.widgets import Pretty, Static, TabbedContent

from .datatable_nav import DataTableNav, SelectionChanged


class Secrets(Static):
    BORDER_TITLE = "Secrets"

    BINDINGS = [
        ("a", "add", "Add"),
        ("d", "delete", "Delete"),
        ("r", "rename", "Rename"),
    ]

    def __init__(self, num: int, control_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._control_id = control_id
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="secrets-dt", filter_field="Name")
        self.table.add_column("Name", key="Name")
        self.table.add_rows([["Secret 1"], ["Secret 2"]])
        yield self.table

    def on_data_table_row_selected(self, message):
        self.post_message(
            SelectionChanged(control_id=self._control_id, row_key=message.row_key)
        )


class SecretsInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Secrets Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Secret": "Content"})
