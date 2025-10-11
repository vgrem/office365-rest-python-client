from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.webappexturlpair import WebAppExtUrlPair


class WebAppUrlsByAction(ClientValue):

    def __init__(
        self,
        action: str = None,
        urls_by_ext: ClientValueCollection[WebAppExtUrlPair] = ClientValueCollection(WebAppExtUrlPair),
    ):
        self.Action = action
        self.UrlsByExt = urls_by_ext

    @property
    def entity_type_name(self):
        return "SP.Utilities.WebAppUrlsByAction"
