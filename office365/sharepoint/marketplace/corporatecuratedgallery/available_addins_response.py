from __future__ import annotations


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.instance_info import (
    SPAddinInstanceInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


@dataclass
class SPAvailableAddinsResponse(ClientValue):

    addins: ClientValueCollection[SPAddinInstanceInfo] | None = None
    errorsWithServerRelativeUrl: ClientValueCollection[SPErrorWithServerRelativeUrl] = ClientValueCollection(SPErrorWithServerRelativeUrl)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAvailableAddinsResponse"