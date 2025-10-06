from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spaddinprincipalinfo import (
    SPAddinPrincipalInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


class SPGetAddinPrincipalsResponse(ClientValue):

    def __init__(
        self,
        addin_principals: ClientValueCollection[
            SPAddinPrincipalInfo
        ] = ClientValueCollection(SPAddinPrincipalInfo),
        errors_with_server_relative_url: ClientValueCollection[
            SPErrorWithServerRelativeUrl
        ] = ClientValueCollection(SPErrorWithServerRelativeUrl),
    ):
        self.addinPrincipals = addin_principals
        self.errorsWithServerRelativeUrl = errors_with_server_relative_url

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPGetAddinPrincipalsResponse"
