from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.alerts.securityresourcetype import (
    SecurityResourceType,
)


@value
class SecurityResource(ClientValue):
    resource: str | None = None
    resourceType: SecurityResourceType = SecurityResourceType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SecurityResource"
