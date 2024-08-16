from textual.app import ComposeResult
from textual.widgets import Pretty, Static, TabbedContent

from .datatable_nav import DataTableNav, SelectionChanged


class Nodes(Static):
    BORDER_TITLE = "Nodes"

    BINDINGS = [
        ("w", "worker", "Worker Token"),
        ("m", "manager", "Manger Token"),
    ]

    def __init__(self, num: int, control_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._control_id = control_id
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="nodes-dt", filter_field="Name")
        self.table.add_column("Name", key="Name")
        self.table.add_rows([["manager1"], ["worker1"]])
        yield self.table

    def on_data_table_row_selected(self, message):
        self.post_message(
            SelectionChanged(control_id=self._control_id, row_key=message.row_key)
        )


class NodeInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Node Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Nodes": "Content"})
