from office365.runtime.client_value import ClientValue


class DomainRestrictionSettings(ClientValue):
    def __init__(
        self,
        domain_restriction_mode: int = None,
        domain_restriction_mode_at_site: int = None,
        restricted_domains: str = None,
        restricted_domains_at_site: str = None,
    ):
        self.domainRestrictionMode = domain_restriction_mode
        self.domainRestrictionModeAtSite = domain_restriction_mode_at_site
        self.restrictedDomains = restricted_domains
        self.restrictedDomainsAtSite = restricted_domains_at_site

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.DomainRestrictionSettings"
