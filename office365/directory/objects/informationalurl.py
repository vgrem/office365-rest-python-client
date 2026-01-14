from office365.runtime.client_value import ClientValue


class InformationalUrl(ClientValue):
    def __init__(
        self,
        logo_url: str = None,
        marketing_url: str = None,
        privacy_statement_url: str = None,
        support_url: str = None,
        terms_of_service_url: str = None,
    ):
        self.logoUrl = logo_url
        self.marketingUrl = marketing_url
        self.privacyStatementUrl = privacy_statement_url
        self.supportUrl = support_url
        self.termsOfServiceUrl = terms_of_service_url

    @property
    def entity_type_name(self):
        return "microsoft.graph.InformationalUrl"
