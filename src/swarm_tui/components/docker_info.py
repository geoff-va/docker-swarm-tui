from textual.app import ComposeResult
from textual.widgets import Pretty, Static, TabbedContent


class DockerInfo(Static):
    BINDINGS = [
        ("f", "fullscreen", "Toggle Fullscreen"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent("Info"):
            yield Pretty({"Docker": "Info"})
