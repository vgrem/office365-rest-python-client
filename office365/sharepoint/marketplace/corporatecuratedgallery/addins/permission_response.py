from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.permission_failed_info import (
    SPAddinPermissionFailedInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.permission_info import (
    SPAddinPermissionInfo,
)


class SPAddinPermissionResponse(ClientValue):
    addinPermissions: ClientValueCollection[SPAddinPermissionInfo] = field(
        default_factory=lambda: ClientValueCollection(SPAddinPermissionInfo)
    )
    failedAddins: ClientValueCollection[SPAddinPermissionFailedInfo] = field(
        default_factory=lambda: ClientValueCollection(SPAddinPermissionFailedInfo)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionResponse"
