from typing import Protocol


class FilterableWidget(Protocol):
    def init_filter(self) -> None:
        raise NotImplementedError

    def filter(self, text: str) -> None:
        raise NotImplementedError

    def clear_filter(self) -> None:
        raise NotImplementedError
