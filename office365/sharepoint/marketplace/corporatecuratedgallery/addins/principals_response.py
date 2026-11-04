from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.marketplace.corporatecuratedgallery.spaddinprincipalinfo import (
    SPAddinPrincipalInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


@value
class SPGetAddinPrincipalsResponse(ClientValue):
    addinPrincipals: ClientValueCollection[SPAddinPrincipalInfo] = field(
        default_factory=lambda: ClientValueCollection(SPAddinPrincipalInfo)
    )
    errorsWithServerRelativeUrl: ClientValueCollection[SPErrorWithServerRelativeUrl] = field(
        default_factory=lambda: ClientValueCollection(SPErrorWithServerRelativeUrl)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPGetAddinPrincipalsResponse"
