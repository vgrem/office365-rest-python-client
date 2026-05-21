from __future__ import annotations


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.permission_failed_info import (
    SPAddinPermissionFailedInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.permission_info import (
    SPAddinPermissionInfo,
)


@dataclass
class SPAddinPermissionResponse(ClientValue):

    addinPermissions: ClientValueCollection[SPAddinPermissionInfo] | None = None
    failedAddins: ClientValueCollection[SPAddinPermissionFailedInfo] | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionResponse"