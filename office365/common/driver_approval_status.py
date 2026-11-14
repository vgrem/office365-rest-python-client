from __future__ import annotations

from enum import Enum


class DriverApprovalStatus(Enum):
    needsReview = "0"
    declined = "1"
    approved = "2"
    suspended = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriverApprovalStatus"
