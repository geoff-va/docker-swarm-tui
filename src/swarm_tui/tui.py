import logging

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import ContentSwitcher, Footer, Header

from swarm_tui.components.config import Config, ConfigInfo
from swarm_tui.components.datatable_nav import SelectionChanged
from swarm_tui.components.docker_info import DockerInfo
from swarm_tui.components.nodes import NodeInfo, Nodes
from swarm_tui.components.secrets import Secrets, SecretsInfo
from swarm_tui.components.stacks import StackInfo, Stacks

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
                yield Stacks(1)
                yield Config(2, "config-info")
                yield Secrets(3, "secrets-info")
                yield Nodes(4, "node-info")
            with Vertical(id="right"):
                # FIX: Create some kind of default panel that shows defaul info
                with ContentSwitcher(id="info-pane", initial="docker-info"):
                    yield DockerInfo(id="docker-info")
                    yield StackInfo(id="stack-info")
                    yield ConfigInfo(id="config-info")
                    yield SecretsInfo(id="secrets-info")
                    yield NodeInfo(id="node-info")
        yield Footer()

    def on_selection_changed(self, message: SelectionChanged):
        self.query_one("#info-pane", ContentSwitcher).current = message.control_id
        self.log.info(f"{message.selected_id.value=}")


def tui():
    app = SwarmTui()
    app.run()


if __name__ == "__main__":
    tui()
