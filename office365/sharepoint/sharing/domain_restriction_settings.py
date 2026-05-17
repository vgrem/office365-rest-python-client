from typing import Optional

from office365.runtime.client_value import ClientValue


class DomainRestrictionSettings(ClientValue):
    def __init__(
        self,
        domain_restriction_mode: Optional[int] = None,
        domain_restriction_mode_at_site: Optional[int] = None,
        restricted_domains: Optional[str] = None,
        restricted_domains_at_site: Optional[str] = None,
    ):
        self.domainRestrictionMode = domain_restriction_mode
        self.domainRestrictionModeAtSite = domain_restriction_mode_at_site
        self.restrictedDomains = restricted_domains
        self.restrictedDomainsAtSite = restricted_domains_at_site

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.DomainRestrictionSettings"
