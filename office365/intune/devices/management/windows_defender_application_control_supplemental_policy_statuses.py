from __future__ import annotations

from enum import Enum


class WindowsDefenderApplicationControlSupplementalPolicyStatuses(Enum):
    unknown = "0"
    success = "1"
    tokenError = "2"
    notAuthorizedByToken = "3"
    policyNotFound = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderApplicationControlSupplementalPolicyStatuses"
