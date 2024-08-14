from textual.app import ComposeResult
from textual.widgets import Static

from .datatable_nav import DataTableNav


class Tasks(Static):
    BORDER_TITLE = "Tasks"

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="tasks-dt", filter_field="Name")
        self.table.cursor_type = "row"
        self.table.add_column("Name", key="Name")
        yield self.table
