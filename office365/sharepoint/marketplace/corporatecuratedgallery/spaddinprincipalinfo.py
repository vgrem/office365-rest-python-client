from typing import Optional

from office365.runtime.client_value import ClientValue


class SPAddinPrincipalInfo(ClientValue):
    absoluteUrl: Optional[str] = None
    appIdentifier: Optional[str] = None
    serverRelativeUrl: Optional[str] = None
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPrincipalInfo"
