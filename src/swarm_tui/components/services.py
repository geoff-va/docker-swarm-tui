from textual.app import ComposeResult
from textual.widgets import Static

from .datatable_nav import DataTableNav


class Services(Static):
    BORDER_TITLE = "Services"

    def compose(self) -> ComposeResult:
        self.table = DataTableNav(id="services-dt", filter_field="Name")
        self.table.cursor_type = "row"
        self.table.add_column("Name", key="Name")
        yield self.table
