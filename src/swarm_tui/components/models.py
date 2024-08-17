from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SelectedContent:
    selected_id: str
    data: Any
