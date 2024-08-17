from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, Static, TabbedContent

from .datatable_nav import DataTableNav
from .navigable_panel import NavigablePanel


class Nodes(NavigablePanel):
    BORDER_TITLE = "Nodes"

    BINDINGS = [
        ("w", "worker", "Worker Token"),
        ("m", "manager", "Manger Token"),
    ]

    data: reactive[list[str]] = reactive([])

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="nodes-dt", filter_field="Name")
        self.table.add_column("Name", key="Name")
        yield self.table

    def watch_data(self, rows: list[str]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(row, key=row)
        self.table.sort("Name", key=lambda x: x.lower())


class NodeInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Page 1", "Page 2") as tc:
            tc.border_title = "Node Info"
            yield Pretty({"Info": "Content"})
            yield Pretty({"Nodes": "Content"})
