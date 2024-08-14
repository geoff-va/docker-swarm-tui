from textual.app import ComposeResult
from textual.widgets import Static, TabbedContent, TextArea


class Info(Static):
    BORDER_TITLE = "Info"

    def compose(self) -> ComposeResult:
        with TabbedContent("Info"):
            yield TextArea()
