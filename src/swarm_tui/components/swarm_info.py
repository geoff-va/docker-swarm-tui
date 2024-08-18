import json

from textual import work
from textual.app import ComposeResult
from textual.widgets import Static, TabbedContent, TextArea

from ..backends.base import BaseBackend
from ..exceptions import DockerApiError


class SwarmInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def __init__(self, backend: BaseBackend, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        self.component = TextArea(read_only=True, language="json")
        with TabbedContent("Info") as tc:
            tc.border_title = "Swarm Info"
            yield self.component

    @work
    async def load_swarm_info(self) -> None:
        try:
            info = await self.backend.get_swarm_info()
            self.component.text = json.dumps(info, indent=2, sort_keys=True)
        except DockerApiError as e:
            self.notify(str(e), severity="error")
            self.component.text = "{}"
