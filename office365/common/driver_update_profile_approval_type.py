from __future__ import annotations

from enum import Enum


class DriverUpdateProfileApprovalType(Enum):
    manual = "0"
    automatic = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriverUpdateProfileApprovalType"
