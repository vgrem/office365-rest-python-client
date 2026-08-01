from __future__ import annotations

from enum import Enum


class Windows365SwitchCompatibilityFailureReasonType(Enum):
    osVersionNotSupported = "0"
    hardwareNotSupported = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows365SwitchCompatibilityFailureReasonType"
