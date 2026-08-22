from __future__ import annotations

from office365.runtime.client_value import ClientValue


class VerifiedDomain(ClientValue):
    """Specifies a domain for a tenant. The verifiedDomains property of the organization entity is a collection of"
    verifiedDomain objects"""

    capabilities: str | None = None
    isDefault: bool | None = None
    isInitial: bool | None = None
    name: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VerifiedDomain"
