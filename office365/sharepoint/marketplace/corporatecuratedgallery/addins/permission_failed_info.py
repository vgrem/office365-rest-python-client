from typing import Optional

from office365.runtime.client_value import ClientValue


class SPAddinPermissionFailedInfo(ClientValue):
    appIdentifier: Optional[str] = None
    errorMessage: Optional[str] = None
    serverRelativeUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionFailedInfo"
