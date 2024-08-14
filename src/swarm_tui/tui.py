from __future__ import annotations

import logging

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from swarm_tui.components.config import Config
from swarm_tui.components.info import Info
from swarm_tui.components.secrets import Secrets
from swarm_tui.components.services import Services
from swarm_tui.components.stacks import Stacks
from swarm_tui.components.tasks import Tasks

log = logging.getLogger(__name__)


class SwarmTui(App):
    """A TUI interface for swram management"""

    AUTO_FOCUS = ""

    CSS_PATH = "./tui.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left"):
                yield Stacks()
                yield Config()
                yield Secrets()
            with Vertical(id="right"):
                yield Info()
        yield Footer()


def tui():
    app = SwarmTui()
    app.run()


if __name__ == "__main__":
    tui()
