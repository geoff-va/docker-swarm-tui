from __future__ import annotations

from typing import Any

from textual.binding import Binding
from textual.message import Message
from textual.widgets import DataTable

from .filter import DtFilter, StartFiltering, StopFiltering


class SelectionChanged(Message):
    def __init__(self, control_id: str, selected_id: str) -> None:
        self.control_id = control_id
        self.selected_id = selected_id
        super().__init__()


class DataTableNav(DataTable):
    """A Filterable DataTable /w more vim-like nav bindings"""

    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("h", "cursor_left", "Cursor Left", show=False),
        Binding("l", "cursor_right", "Cursor Right", show=False),
        Binding("escape", "cancel", "Cancel"),
        Binding("/", "start_filtering", "Filter"),
    ]
    filter_class = DtFilter

    def __init__(
        self,
        filter_field: str = "",
        hide_cursor_on_focus_change: bool = True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._filter_field = filter_field
        self._hide_cursor_on_focus_change = hide_cursor_on_focus_change
        if hide_cursor_on_focus_change:
            self.cursor_type = "none"

    def action_start_filtering(self) -> None:
        """Start Filtering"""
        if self._filter_field:
            self.post_message(StartFiltering(widget=self))

    def action_cancel(self) -> None:
        """Stop Filtering"""
        if self._filter_field:
            self.post_message(StopFiltering())

    def init_filter(self) -> None:
        self._filter = self.filter_class(self, self._filter_field)
        self._filter.init_filter()

    def filter(self, text: str) -> None:
        self._filter.filter(text)

    def clear_filter(self) -> None:
        self._filter.clear_filter()

    def on_focus(self) -> None:
        if self._hide_cursor_on_focus_change:
            self.cursor_type = "row"

    def on_blur(self) -> None:
        if self._hide_cursor_on_focus_change:
            self.cursor_type = "none"
