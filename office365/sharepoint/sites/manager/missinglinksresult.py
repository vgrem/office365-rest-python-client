from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.missinglink import MissingLink


class MissingLinksResult(ClientValue):

    def __init__(
        self,
        missing_links: ClientValueCollection[MissingLink] = ClientValueCollection(MissingLink),
    ):
        self.MissingLinks = missing_links

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLinksResult"
