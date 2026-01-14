from office365.runtime.client_value import ClientValue


class EmailSettings(ClientValue):
    def __init__(self, sender_domain: str = None, use_company_branding: bool = None):
        self.senderDomain = sender_domain
        self.useCompanyBranding = use_company_branding

    @property
    def entity_type_name(self):
        return "microsoft.graph.EmailSettings"
