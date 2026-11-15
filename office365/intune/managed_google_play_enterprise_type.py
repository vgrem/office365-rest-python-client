from __future__ import annotations

from enum import Enum


class ManagedGooglePlayEnterpriseType(Enum):
    enterpriseTypeUnspecified = "0"
    managedGoogleDomain = "1"
    managedGooglePlayAccountsEnterprise = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedGooglePlayEnterpriseType"
