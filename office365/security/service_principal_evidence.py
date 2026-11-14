from __future__ import annotations

from office365.security.alerts.evidence import AlertEvidence
from office365.security.service_principal_type import ServicePrincipalType


class ServicePrincipalEvidence(AlertEvidence):
    appId: str | None = None
    appOwnerTenantId: str | None = None
    servicePrincipalName: str | None = None
    servicePrincipalObjectId: str | None = None
    tenantId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ServicePrincipalEvidence"

    servicePrincipalType: ServicePrincipalType = ServicePrincipalType.unknown
