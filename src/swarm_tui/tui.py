from __future__ import annotations

import logging

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

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
        yield Footer()


def tui():
    app = SwarmTui()
    app.run()


if __name__ == "__main__":
    tui()
