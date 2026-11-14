from __future__ import annotations

from enum import Enum


class WindowsManagedAppClipboardSharingLevel(Enum):
    anyDestinationAnySource = "0"
    none = "1"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagedAppClipboardSharingLevel"
