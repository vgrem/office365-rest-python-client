from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.instance_info import (
    SPAddinInstanceInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


@value
class SPAvailableAddinsResponse(ClientValue):
    addins: ClientValueCollection[SPAddinInstanceInfo] = field(
        default_factory=lambda: ClientValueCollection(SPAddinInstanceInfo)
    )
    errorsWithServerRelativeUrl: ClientValueCollection[SPErrorWithServerRelativeUrl] = field(
        default_factory=lambda: ClientValueCollection(SPErrorWithServerRelativeUrl)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAvailableAddinsResponse"
