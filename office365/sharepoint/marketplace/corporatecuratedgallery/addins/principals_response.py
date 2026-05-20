from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spaddinprincipalinfo import (
    SPAddinPrincipalInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


@dataclass
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
