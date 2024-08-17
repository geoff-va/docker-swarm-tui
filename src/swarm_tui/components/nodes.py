from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, TabbedContent

from .datatable_nav import DataTableNav
from .info_panel import InfoPanel
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
        self.table.show_header = False
        self.table.add_column("Name", key="Name")
        yield self.table

    def watch_data(self, rows: list[str]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(row, key=row)
        self.table.sort("Name", key=lambda x: x.lower())


class NodeInfo(InfoPanel):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        self.component = Pretty({})
        with TabbedContent("Info"):
            yield self.component

    async def watch_selected(self, selected: str) -> None:
        self.query_one(TabbedContent).border_title = f"Node: {selected}"
        info = await self.backend.get_node_info(selected)
        self.component.update(info)
