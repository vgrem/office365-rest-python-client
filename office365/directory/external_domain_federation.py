from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.identity_source import IdentitySource


class ExternalDomainFederation(IdentitySource):
    displayName: str | None = None
    domainName: str | None = None
    issuerUri: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExternalDomainFederation"
