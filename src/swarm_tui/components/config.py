from textual.app import ComposeResult
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import Pretty, Static, TabbedContent, TextArea

from .datatable_nav import DataTableNav, SelectionChanged


class Config(Static):
    BORDER_TITLE = "Config"

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
        self.table = DataTableNav(id="config-dt", filter_field="Name")
        self.table.cursor_type = "none"
        self.table.add_column("Name", key="Name")
        self.table.add_rows([["Config 1"], ["Config 2"]])
        self.table.move_cursor()
        yield self.table

    def on_data_table_row_selected(self, message):
        self.post_message(
            SelectionChanged(control_id=self._control_id, row_key=message.row_key)
        )


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
