from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class ActiveDirectoryDomainEvidence(ClientValue):
    activeDirectoryDomainName: str | None = None
    trustedDomains: ClientValueCollection[ActiveDirectoryDomainEvidence] = field(
        default_factory=lambda: ClientValueCollection(ActiveDirectoryDomainEvidence)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ActiveDirectoryDomainEvidence"
