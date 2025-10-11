from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.addins.instance_info import (
    SPAddinInstanceInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.sperrorwithserverrelativeurl import (
    SPErrorWithServerRelativeUrl,
)


class SPAvailableAddinsResponse(ClientValue):

    def __init__(
        self,
        addins=None,
        errors_with_server_relative_url: ClientValueCollection[SPErrorWithServerRelativeUrl] = ClientValueCollection(
            SPErrorWithServerRelativeUrl
        ),
    ):
        self.addins = ClientValueCollection(SPAddinInstanceInfo, addins)
        self.errorsWithServerRelativeUrl = errors_with_server_relative_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAvailableAddinsResponse"
