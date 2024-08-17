import logging

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import ContentSwitcher, Footer, Header

from swarm_tui.backends.base import BaseBackend
from swarm_tui.backends.fake import FakeBackend
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

    def __init__(self, backend: BaseBackend, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left"):
                yield Stacks(1)
                yield Config(2, "config-info")
                yield Secrets(3, "secrets-info")
                yield Nodes(4, "node-info")
            with Vertical(id="right"):
                with ContentSwitcher(id="info-pane", initial="docker-info"):
                    yield DockerInfo(id="docker-info")
                    yield StackInfo(id="stack-info")
                    yield ConfigInfo(self.backend, id="config-info")
                    yield SecretsInfo(self.backend, id="secrets-info")
                    yield NodeInfo(id="node-info")
        yield Footer()

    def on_mount(self) -> None:
        self.load_secrets()
        self.load_nodes()
        self.load_configs()
        self.load_stacks_and_services()

    @work
    async def load_secrets(self) -> None:
        self.query_one(Secrets).data = await self.backend.get_secrets()

    @work
    async def load_nodes(self) -> None:
        self.query_one(Nodes).data = await self.backend.get_nodes()

    @work
    async def load_configs(self) -> None:
        self.query_one(Config).data = await self.backend.get_configs()

    @work
    async def load_stacks_and_services(self) -> None:
        stacks, services = await self.backend.get_stacks_and_services()
        self.query_one(Stacks).stacks = stacks
        self.query_one(Stacks).services = services

    async def on_selection_changed(self, message: SelectionChanged):
        info = self.query_one(f"#{message.control_id}")
        info.selected = message.selected_id.value
        self.query_one("#info-pane", ContentSwitcher).current = message.control_id
        self.log.info(f"{message.selected_id.value=}")


def tui():
    backend = FakeBackend()
    app = SwarmTui(backend)
    app.run()


if __name__ == "__main__":
    tui()
