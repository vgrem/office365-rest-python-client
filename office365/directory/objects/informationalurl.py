from typing import Optional

from office365.runtime.client_value import ClientValue


class InformationalUrl(ClientValue):
    def __init__(
        self,
        logo_url: Optional[str] = None,
        marketing_url: Optional[str] = None,
        privacy_statement_url: Optional[str] = None,
        support_url: Optional[str] = None,
        terms_of_service_url: Optional[str] = None,
    ):
        self.logoUrl = logo_url
        self.marketingUrl = marketing_url
        self.privacyStatementUrl = privacy_statement_url
        self.supportUrl = support_url
        self.termsOfServiceUrl = terms_of_service_url

    @property
    def entity_type_name(self):
        return "microsoft.graph.InformationalUrl"
