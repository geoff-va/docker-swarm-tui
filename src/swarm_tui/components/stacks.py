from textual.app import ComposeResult
from textual.widgets import RichLog, Static, TabbedContent, TextArea, Tree

from .datatable_nav import DataTableNav


class Stacks(Static):
    BORDER_TITLE = "Stacks"

    BINDINGS = [
        ("e", "expand", "Expand All"),
        ("c", "collapse", "Collapse All"),
    ]

    def __init__(self, num: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        tree1: Tree[dict] = Tree("ibl-dm-pro (2)")
        tree1.root.expand()
        db = tree1.root.add("db (1/1)")
        db.add_leaf("db.1")
        web = tree1.root.add("web (3/3)", expand=True)
        web.add_leaf("web.1")
        web.add_leaf("web.2")
        web.add_leaf("web.3")
        yield tree1

        tree2: Tree[dict] = Tree("--")
        tree2.root.expand()
        db2 = tree2.root.add("db (1/1)")
        db2.add_leaf("db.1")
        web = tree2.root.add("web (3/3)", expand=True)
        web.add_leaf("service.1")
        web.add_leaf("service.2")
        web.add_leaf("service.3")
        yield tree2


class StackInfo(Static):
    BORDER_TITLE = "Stack Info"

    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Info", "Logs", "Volumes"):
            yield TextArea("Content")
            yield RichLog()
            yield TextArea()
