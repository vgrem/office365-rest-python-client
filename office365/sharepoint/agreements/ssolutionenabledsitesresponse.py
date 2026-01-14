from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.site import SPAgreementsSite


class AgreementsSolutionEnabledSitesResponse(ClientValue):
    def __init__(
        self,
        sites: ClientValueCollection[SPAgreementsSite] = None,
        skip_token: str = None,
    ):
        self.sites = sites
        self.skip_token = skip_token
