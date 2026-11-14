from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class UserExperienceAnalyticsDeviceScopeSummary(ClientValue):
    completedDeviceScopeIds: StringCollection = field(default_factory=StringCollection)
    insufficientDataDeviceScopeIds: StringCollection = field(default_factory=StringCollection)
    totalDeviceScopes: int | None = None
    totalDeviceScopesEnabled: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceScopeSummary"
