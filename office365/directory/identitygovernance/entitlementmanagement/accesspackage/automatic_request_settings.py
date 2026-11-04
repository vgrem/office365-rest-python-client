from __future__ import annotations

from datetime import timedelta

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AccessPackageAutomaticRequestSettings(ClientValue):
    gracePeriodBeforeAccessRemoval: timedelta | None = None
    removeAccessWhenTargetLeavesAllowedTargets: bool | None = None
    requestAccessForAllowedTargets: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAutomaticRequestSettings"
