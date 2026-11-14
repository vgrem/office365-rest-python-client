from __future__ import annotations

from enum import Enum


class WindowsDriverUpdateProfileInventorySyncState(Enum):
    pending = "0"
    success = "1"
    failure = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDriverUpdateProfileInventorySyncState"
