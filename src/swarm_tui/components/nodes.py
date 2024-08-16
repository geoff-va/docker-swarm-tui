from textual.app import ComposeResult
from textual.widgets import Pretty, Static, TabbedContent

from .datatable_nav import DataTableNav, SelectionChanged
from .navigable_panel import NavigablePanel


class Nodes(NavigablePanel):
    BORDER_TITLE = "Nodes"

    BINDINGS = [
        ("w", "worker", "Worker Token"),
        ("m", "manager", "Manger Token"),
    ]

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="nodes-dt", filter_field="Name")
        self.table.add_column("Name", key="Name")
        self.table.add_row("manager 1", key="manager 1")
        self.table.add_row("worker 1", key="worker 1")
        yield self.table


class NodeInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Node Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Nodes": "Content"})
