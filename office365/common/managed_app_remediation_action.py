from __future__ import annotations

from enum import Enum


class ManagedAppRemediationAction(Enum):
    block = "0"
    wipe = "1"
    warn = "2"
    blockWhenSettingIsSupported = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppRemediationAction"
