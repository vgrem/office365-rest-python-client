from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from office365.runtime.client_value import ClientValue


@dataclass
class AccessPackageAutomaticRequestSettings(ClientValue):
    gracePeriodBeforeAccessRemoval: timedelta | None = None
    removeAccessWhenTargetLeavesAllowedTargets: bool | None = None
    requestAccessForAllowedTargets: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAutomaticRequestSettings"
