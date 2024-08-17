from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Pretty, Static, TabbedContent

from ..backends.base import BaseBackend


class InfoPanel(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    selected: reactive[str | None] = reactive(None)

    def __init__(self, backend: BaseBackend, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        self.component = Pretty({})
        with TabbedContent("Info"):
            yield self.component
