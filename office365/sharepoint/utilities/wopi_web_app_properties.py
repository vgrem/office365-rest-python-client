from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.webappurlsbyaction import WebAppUrlsByAction
from typing import Optional


class WopiWebAppProperties(ClientValue):
    def __init__(
        self,
        app: Optional[str] = None,
        bootstrapper_url: Optional[str] = None,
        list_by_action: ClientValueCollection[WebAppUrlsByAction] = ClientValueCollection(WebAppUrlsByAction),
    ):
        self.App = app
        self.BootstrapperUrl = bootstrapper_url
        self.ListByAction = list_by_action

    @property
    def entity_type_name(self):
        return "SP.Utilities.WopiWebAppProperties"
