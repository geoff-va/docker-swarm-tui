from textual.app import ComposeResult
from textual.widgets import Static, Tree

from .datatable_nav import DataTableNav


class Stacks(Static):
    BORDER_TITLE = "Stacks"

    def compose(self) -> ComposeResult:
        tree1: Tree[dict] = Tree("ibl-dm-pro (2)")
        tree1.root.expand()
        tree1.root.add("db (1/1)")
        web = tree1.root.add("web (3/3)", expand=True)
        web.add_leaf("web.1")
        web.add_leaf("web.2")
        web.add_leaf("web.3")
        yield tree1

        tree2: Tree[dict] = Tree("--")
        tree2.root.expand()
        tree2.root.add("db (1/1)")
        web = tree2.root.add("web (3/3)", expand=True)
        web.add_leaf("service.1")
        web.add_leaf("service.2")
        web.add_leaf("service.3")
        yield tree2
