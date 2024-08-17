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

    stacks_and_services: reactive[tuple[list[models.Stack], list[models.Service]]] = (
        reactive(([], []))
    )

    def __init__(self, num: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        self.stack_tree: Tree[models.DockerNode] = Tree("Stacks")
        self.stack_tree.guide_depth = 3
        self.stack_tree.show_root = False
        yield self.stack_tree

    def watch_stacks_and_services(
        self, stacks_and_services: tuple[list[models.Stack], list[models.Service]]
    ) -> None:
        stacks, services = stacks_and_services
        self.stack_tree.clear()
        for stack in stacks:
            stack_node = self.stack_tree.root.add(
                f"📚 {stack.name} ({len(stack.services)})", data=stack
            )
            for service in stack.services:
                service_node = stack_node.add(f"⍾ {service.name}", data=service)
                for task in service.tasks:
                    service_node.add_leaf(task.name, data=task)

        for service in services:
            service_node = self.stack_tree.root.add(f"⍾ {service.name}", data=service)
            for task in service.tasks:
                service_node.add_leaf(task.name, data=task)


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
