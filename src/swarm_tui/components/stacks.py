from textual.app import ComposeResult
from textual.widgets import RichLog, Static, TabbedContent, TextArea, Tree

from .datatable_nav import DataTableNav


class Stacks(Static):
    """Stacks and Services Panel

    - Stacks have a special prefix/icon
    - Services have a different one
    """

    BORDER_TITLE = "Stacks and Services"

    BINDINGS = [
        ("e", "expand", "Expand All"),
        ("c", "collapse", "Collapse All"),
    ]

    def __init__(self, num: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Stacks")
        tree.guide_depth = 3
        tree.show_root = False
        stack1 = tree.root.add("ibl-dm-pro (2)")
        db = stack1.add("db (1/1)")
        db.add_leaf("db.1")
        web = stack1.add("web (3/3)")
        web.add_leaf("web.1")
        web.add_leaf("web.2")
        web.add_leaf("web.3")

        stack2 = tree.root.add("other-stack (1)")
        service = stack2.add("service (1/1)")
        service.add_leaf("service.1")

        unbound = tree.root.add("service (1/1)")
        unbound.add_leaf("service.1")
        yield tree


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
