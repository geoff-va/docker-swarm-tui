from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import RichLog, Static, TabbedContent, TextArea, Tree

from ..backends import models


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

    stacks: reactive[list[models.Stack]] = reactive([])
    services: reactive[list[models.Service]] = reactive([])

    def __init__(self, num: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        self.stack_tree: Tree[dict] = Tree("Stacks")
        self.stack_tree.guide_depth = 3
        self.stack_tree.show_root = False
        yield self.stack_tree

        self.service_tree: Tree[dict] = Tree("Unbound Services")
        self.service_tree.guide_depth = 3
        self.service_tree.show_root = False
        yield self.service_tree

    def watch_stacks(self, stacks: list[models.Stack]) -> None:
        self.stack_tree.clear()
        for stack in stacks:
            stack_node = self.stack_tree.root.add(
                f"{stack.name} ({len(stack.services)})"
            )
            for service in stack.services:
                service_node = stack_node.add(service.name)
                for task in service.tasks:
                    service_node.add_leaf(task.name)

    def watch_services(self, services: list[models.Service]) -> None:
        self.service_tree.clear()
        for service in services:
            service_node = self.service_tree.root.add(service.name)
            for task in service.tasks:
                service_node.add_leaf(task.name)


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
