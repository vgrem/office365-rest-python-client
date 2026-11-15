from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.evidence.base import AlertEvidence


class ActiveDirectoryDomainEvidence(AlertEvidence):
    activeDirectoryDomainName: str | None = None
    trustedDomains: ClientValueCollection[ActiveDirectoryDomainEvidence] = field(
        default_factory=lambda: ClientValueCollection(ActiveDirectoryDomainEvidence)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ActiveDirectoryDomainEvidence"
