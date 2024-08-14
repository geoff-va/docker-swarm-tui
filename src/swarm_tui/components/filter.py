from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import DataTable, Input, Label, Static
from textual.widgets.data_table import ColumnKey, RowKey

from .filterable_widget import FilterableWidget


class DtFilter:
    """A Naive way to filter DataTable values"""

    def __init__(self, dt: DataTable, field: str | None = None) -> None:
        self._dt = dt
        self._field: ColumnKey = ColumnKey(field)
        self._col_keys_to_idx: dict[ColumnKey, int] = {}
        self._col_index = 0
        self._orig_row_data: list[tuple] = []

    def init_filter(self) -> None:
        """Store the original data, preserving order and row/col information"""
        self._col_keys_to_idx = {
            key: self._dt.get_column_index(key) for key in self._dt.columns
        }
        data = []
        for rowkey in self._dt.rows:
            idx = self._dt.get_row_index(rowkey)
            data.append((idx, rowkey.value, self._dt.get_row(rowkey)))
        self._orig_row_data = sorted(data, key=lambda x: x[0])
        self._col_index = (
            0 if self._field is None else self._col_keys_to_idx[self._field]
        )

    def filter(self, text: str) -> None:
        """Super naive text matching"""
        self._dt.clear()
        for _, rowkey, data in self._orig_row_data:
            if text in data[self._col_index]:
                self._dt.add_row(*data, key=rowkey)

    def clear_filter(self) -> None:
        """Clear the filtered data and restore the original"""
        hl_row, hl_col = self._get_highlighted_keys()
        self._restore_original_data()
        self._restore_selection(hl_row, hl_col)

    def _get_highlighted_keys(self) -> tuple[RowKey | None, ColumnKey | None]:
        """Return the currently highlighted cell"""
        if self._dt.is_valid_coordinate(self._dt.cursor_coordinate):
            return self._dt.coordinate_to_cell_key(self._dt.cursor_coordinate)
        return None, None

    def _restore_original_data(self) -> None:
        """Restore the original data to the datatable"""
        self._dt.clear()
        for _, rowkey, data in self._orig_row_data:
            self._dt.add_row(*data, key=rowkey)

    def _restore_selection(
        self, hl_row: RowKey | None, hl_col: ColumnKey | None
    ) -> None:
        """Highlight the currently highlighted row if one exists"""
        if hl_row is not None and hl_col is not None:
            self._dt.cursor_coordinate = self._dt.get_cell_coordinate(hl_row, hl_col)


class Filter(Static):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def action_cancel(self) -> None:
        """Stop Filtering"""
        self.post_message(StopFiltering())

    def __init__(self, widget: FilterableWidget, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.widget.init_filter()

    def compose(self) -> ComposeResult:
        self._input = Input(id="filter-input")
        with Horizontal():
            yield Label("Filter:", id="filter-label")
            yield self._input

    async def on_input_changed(self, event: Input.Changed) -> None:
        self.run_worker(self.do_filter(event.value), exclusive=True)

    async def do_filter(self, text: str) -> None:
        self.widget.filter(text)

    async def clear_filter(self) -> None:
        self.widget.clear_filter()

    async def on_input_submitted(self) -> None:
        self.widget.focus()

    def focus_input(self) -> None:
        """Sets focus to input widget"""
        self._input.focus()


class StartFiltering(Message):
    def __init__(self, widget: FilterableWidget) -> None:
        super().__init__()
        self.widget = widget


class StopFiltering(Message):
    def __init__(self) -> None:
        super().__init__()
