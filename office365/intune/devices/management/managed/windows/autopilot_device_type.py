from __future__ import annotations

from enum import Enum


class WindowsAutopilotDeviceType(Enum):
    windowsPc = "0"
    holoLens = "1"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsAutopilotDeviceType"
