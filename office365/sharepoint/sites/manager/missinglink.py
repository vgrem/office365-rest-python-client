from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.missinglinkreferrer import MissingLinkReferrer


class MissingLink(ClientValue):
    def __init__(
        self,
        hits: int = None,
        not_found_url: str = None,
        referrers: ClientValueCollection[MissingLinkReferrer] = ClientValueCollection(MissingLinkReferrer),
    ):
        self.Hits = hits
        self.NotFoundUrl = not_found_url
        self.Referrers = referrers

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLink"
