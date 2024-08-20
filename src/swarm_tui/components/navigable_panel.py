from textual.widgets import Static

from ..backends.base import BaseBackend
from .datatable_nav import SelectionChanged


class NavigablePanel(Static):
    """Panel that has an integer identifier and be emit a SelectionChanged message"""

    def __init__(
        self, backend: BaseBackend, num: int, control_id: str, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.backend = backend
        self._control_id = control_id
        if self.BORDER_TITLE:
            self.border_title = f"[{num}] {self.BORDER_TITLE}"

    # FIX: This needs to be generic instead of just for data tables
    # Could be selecting a node in a tree or something else.
    # The data we pass is opaque and is will be forarded to the control
    def on_data_table_row_selected(self, message):
        self.post_message(
            SelectionChanged(
                control_id=self._control_id, selected_id=message.row_key.value
            )
        )

    def focus_child(self) -> None:
        """Focus your appropriate child control"""
        ...
