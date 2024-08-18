import logging

from aiodocker import Docker
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import ContentSwitcher, Footer, Header

from swarm_tui.backends.base import BaseBackend
from swarm_tui.backends.docker import AioDockerBackend
from swarm_tui.backends.fake import FakeBackend
from swarm_tui.components.config import Config, ConfigInfo
from swarm_tui.components.datatable_nav import SelectionChanged
from swarm_tui.components.docker_info import DockerInfo
from swarm_tui.components.info_panel import InfoPanel
from swarm_tui.components.nodes import NodeInfo, Nodes
from swarm_tui.components.secrets import Secrets, SecretsInfo
from swarm_tui.components.stacks import StackInfo, Stacks
from swarm_tui.exceptions import DockerApiError

log = logging.getLogger(__name__)


class SwarmTui(App):
    """A TUI interface for swram management"""

    AUTO_FOCUS = ""
    CSS_PATH = "./tui.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self, backend: BaseBackend, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left"):
                yield Stacks(1, "stack-info")
                yield Config(2, "config-info")
                yield Secrets(3, "secrets-info")
                yield Nodes(4, "node-info")
            with Vertical(id="right"):
                with ContentSwitcher(id="info-pane", initial="docker-info"):
                    yield DockerInfo(id="docker-info")
                    yield StackInfo(self.backend, id="stack-info")
                    yield ConfigInfo(self.backend, id="config-info")
                    yield SecretsInfo(self.backend, id="secrets-info")
                    yield NodeInfo(self.backend, id="node-info")
        yield Footer()

    def action_refresh(self) -> None:
        self.refresh_all()

    def on_mount(self) -> None:
        self.refresh_all()

    def refresh_all(self) -> None:
        self.load_secrets()
        self.load_nodes()
        self.load_configs()
        self.load_stacks_and_services()

    @work
    async def load_secrets(self) -> None:
        try:
            self.query_one(Secrets).data = await self.backend.get_secrets()
        except DockerApiError as e:
            self.notify(title="Error loading secrets", message=str(e), severity="error")
            self.query_one(Secrets).data = []

    @work
    async def load_nodes(self) -> None:
        try:
            self.query_one(Nodes).data = await self.backend.get_nodes()
        except DockerApiError as e:
            self.notify(title="Error loading secrets", message=str(e), severity="error")
            self.query_one(Nodes).data = []

    @work
    async def load_configs(self) -> None:
        try:
            self.query_one(Config).data = await self.backend.get_configs()
        except DockerApiError as e:
            self.notify(title="Error loading secrets", message=str(e), severity="error")
            self.query_one(Config).data = []

    @work
    async def load_stacks_and_services(self) -> None:
        try:
            stacks_and_services = await self.backend.get_stacks_and_services()
            self.query_one(Stacks).stacks_and_services = stacks_and_services
        except DockerApiError as e:
            self.notify(title="Error loading secrets", message=str(e), severity="error")
            self.query_one(Stacks).stacks_and_services = [], []

    async def on_selection_changed(self, message: SelectionChanged):
        info = self.query_one(f"#{message.control_id}", InfoPanel)
        info.loading = True
        info.selected = message.selected_content
        self.query_one("#info-pane", ContentSwitcher).current = message.control_id
        info.loading = False


def tui():
    backend = AioDockerBackend()
    app = SwarmTui(backend)
    app.run()


if __name__ == "__main__":
    tui()
