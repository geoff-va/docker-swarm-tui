from __future__ import annotations

from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, RichLog, Static, TabbedContent, TextArea, Tree

from ..backends import models
from .datatable_nav import SelectionChanged
from .info_panel import InfoPanel
from .models import SelectedContent
from .navigable_panel import NavigablePanel


class Stacks(NavigablePanel):
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
        # TODO: See if we can make "headers" so they aren't selectable
        if stacks:
            self.stack_tree.root.add(
                Text("-- Stack Services --", style="bold cyan"), allow_expand=False
            )
        for stack in stacks:
            stack_node = self.stack_tree.root.add(
                f"📚 {stack.name} ({len(stack.services)})", data=stack
            )
            for service in stack.services:
                service_node = stack_node.add(f"⍾ {service.name}", data=service)
                for task in service.tasks:
                    service_node.add_leaf(task.name, data=task)

        if services:
            self.stack_tree.root.add(
                Text("-- Non-Stack Services --", style="bold cyan"), allow_expand=False
            )

        for service in services:
            service_node = self.stack_tree.root.add(f"⍾ {service.name}", data=service)
            for task in service.tasks:
                service_node.add_leaf(task.name, data=task)

    def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        self.post_message(
            SelectionChanged(
                control_id=self._control_id,
                selected_id=str(message.node.label),
                data=message.node.data,
            )
        )


class StackInfo(InfoPanel):
    BORDER_TITLE = "Stack Info"

    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        self.component = Pretty("(Don't look at me)")
        self.docker_log = RichLog()
        with TabbedContent("Info", "Logs"):
            yield self.component
            yield self.docker_log

    async def watch_selected(self, selected: SelectedContent) -> None:
        if not selected or selected.data is None:
            return
        self.query_one(TabbedContent).border_title = f"Entity: {selected.data.name}"
        info = await self.backend.get_stack_service_info(
            selected.data.name, node_type=selected.data.node_type
        )
        self.component.update(info)
