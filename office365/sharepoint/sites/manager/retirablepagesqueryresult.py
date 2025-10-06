from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.retirablepagemetadata import (
    RetirablePageMetadata,
)


class RetirablePagesQueryResult(ClientValue):

    def __init__(
        self,
        files: ClientValueCollection[RetirablePageMetadata] = ClientValueCollection(
            RetirablePageMetadata
        ),
    ):
        self.Files = files

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.RetirablePagesQueryResult"
