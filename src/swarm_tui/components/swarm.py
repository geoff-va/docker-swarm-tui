from __future__ import annotations

import json

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Label, Static, TabbedContent, TextArea

from ..backends.base import BaseBackend
from ..exceptions import DockerApiError
from . import models
from .datatable_nav import SelectionChanged
from .info_panel import InfoPanel


class FocusedLabel(Label, can_focus=True): ...


class Swarm(Static):
    BORDER_TITLE = "Swarm Info"

    BINDINGS = [
        Binding("w", "worker", "Worker Token"),
        Binding("m", "manager", "Manger Token"),
    ]

    def __init__(
        self, backend: BaseBackend, num: int, control_id: str, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend
        self._control_id = control_id
        if self.BORDER_TITLE:
            self.border_title = f"[{num}] {self.BORDER_TITLE}"

    def compose(self) -> ComposeResult:
        self.swarm_label = FocusedLabel("Docker Swarm")
        yield self.swarm_label

    def focus_child(self) -> None:
        self.swarm_label.focus()

    def on_descendant_focus(self) -> None:
        self.post_message(SelectionChanged(self._control_id, ""))

    async def action_worker(self) -> None:
        # TODO: Create model for user to copy join token/command
        try:
            token = await self.backend.get_worker_token()
            self.notify(message=token, title="Worker Token", severity="information")
        except DockerApiError as e:
            self.notify(str(e), title="Worker Token Error", severity="error")

    async def action_manager(self) -> None:
        # TODO: Create model for user to copy join token/command
        try:
            token = await self.backend.get_manager_token()
            self.notify(message=token, title="Manager Token", severity="information")
        except DockerApiError as e:
            self.notify(str(e), title="Manager Token Error", severity="error")


class SwarmInfo(InfoPanel):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    selected: reactive[models.SelectedContent | None] = reactive(
        None, always_update=True
    )

    def compose(self) -> ComposeResult:
        self.component = TextArea(read_only=True, language="json")
        with TabbedContent("Info") as tc:
            tc.border_title = "Swarm Info"
            yield self.component

    async def watch_selected(self, selected: models.SelectedContent) -> None:
        self.log.info("Launch from watch selected")
        self.load_swarm_info()

    @work
    async def load_swarm_info(self) -> None:
        try:
            info = await self.backend.get_swarm_info()
            self.component.text = json.dumps(info, indent=2, sort_keys=True)
        except DockerApiError as e:
            self.notify(str(e), severity="error")
            self.component.text = "{}"
