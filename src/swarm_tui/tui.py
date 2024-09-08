import logging

from aiodocker import Docker
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import DescendantFocus, Focus
from textual.widgets import ContentSwitcher, Footer, Header

from swarm_tui.backends.base import BaseBackend
from swarm_tui.backends.docker import AioDockerBackend
from swarm_tui.backends.fake import FakeBackend
from swarm_tui.components.config import Config, ConfigInfo
from swarm_tui.components.datatable_nav import SelectionChanged
from swarm_tui.components.info_panel import InfoPanel
from swarm_tui.components.nodes import NodeInfo, Nodes
from swarm_tui.components.secrets import Secrets, SecretsInfo
from swarm_tui.components.stacks import StackInfo, Stacks
from swarm_tui.components.swarm import Swarm, SwarmInfo
from swarm_tui.exceptions import DockerApiError

log = logging.getLogger(__name__)


class SwarmTui(App):
    """A TUI interface for swram management"""

    AUTO_FOCUS = "FocusedLabel"
    CSS_PATH = "./tui.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("1", "focus1", "Focus Swarm", show=False),
        Binding("2", "focus2", "Focus Stacks", show=False),
        Binding("3", "focus3", "Focus Config", show=False),
        Binding("4", "focus4", "Focus Secrets", show=False),
        Binding("5", "focus5", "Focus Nodes", show=False),
    ]

    def __init__(self, backend: BaseBackend, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left"):
                yield Swarm(self.backend, 1, "swarm-info")
                yield Stacks(self.backend, 2, "stack-info")
                yield Config(self.backend, 3, "config-info")
                yield Secrets(self.backend, 4, "secrets-info")
                yield Nodes(self.backend, 5, "node-info")
            with Vertical(id="right"):
                with ContentSwitcher(id="info-pane", initial="swarm-info"):
                    yield SwarmInfo(self.backend, id="swarm-info")
                    yield StackInfo(self.backend, id="stack-info")
                    yield ConfigInfo(self.backend, id="config-info")
                    yield SecretsInfo(self.backend, id="secrets-info")
                    yield NodeInfo(self.backend, id="node-info")
        yield Footer()

    def action_focus1(self) -> None:
        self.query_one(Swarm).focus_child()

    def action_focus2(self) -> None:
        self.query_one(Stacks).focus_child()

    def action_focus3(self) -> None:
        self.query_one(Config).focus_child()

    def action_focus4(self) -> None:
        self.query_one(Secrets).focus_child()

    def action_focus5(self) -> None:
        self.query_one(Nodes).focus_child()

    def action_refresh(self) -> None:
        self.refresh_all()

    def on_mount(self) -> None:
        self.refresh_all()
        self.subscribe_to_events()

    def refresh_all(self) -> None:
        self.load_swarm_info()
        self.load_secrets()
        self.load_nodes()
        self.load_configs()
        self.load_stacks_and_services()

    @work
    async def subscribe_to_events(self):
        self.subscriber = self.backend.get_event_subscriber()
        # TODO: Should probably implement some kind of stop mechanism
        while True:
            event = await self.subscriber.get()
            self.log.debug(f"Docker Event: {event}")
            if event["Type"] == "secret":
                self.load_secrets()
            elif event["Type"] == "config":
                self.load_configs()
            elif event["Type"] == "container":
                self.load_stacks_and_services()

    @work
    async def load_swarm_info(self) -> None:
        try:
            self.query_one(SwarmInfo).load_swarm_info()
        except DockerApiError as e:
            self.notify(
                title="Error loading Swarm Info", message=str(e), severity="error"
            )

    @work
    async def load_secrets(self) -> None:
        await self.query_one(Secrets).reload_table()

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
        self.log.info(f"Selecting: {message.control_id}")
        info = self.query_one(f"#{message.control_id}", InfoPanel)
        info.loading = True
        info.selected = message.selected_content
        self.query_one("#info-pane", ContentSwitcher).current = message.control_id
        info.loading = False


def tui():
    backend = AioDockerBackend()
    # backend = FakeBackend()
    app = SwarmTui(backend)
    app.run()


if __name__ == "__main__":
    tui()
