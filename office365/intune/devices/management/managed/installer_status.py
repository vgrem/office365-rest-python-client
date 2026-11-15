from __future__ import annotations

from enum import Enum


class ManagedInstallerStatus(Enum):
    disabled = "0"
    enabled = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedInstallerStatus"
