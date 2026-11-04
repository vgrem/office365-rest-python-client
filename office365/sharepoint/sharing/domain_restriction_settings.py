from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DomainRestrictionSettings(ClientValue):
    domainRestrictionMode: int | None = None
    domainRestrictionModeAtSite: int | None = None
    restrictedDomains: str | None = None
    restrictedDomainsAtSite: str | None = None

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.DomainRestrictionSettings"
