from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.webappurlsbyaction import WebAppUrlsByAction


@dataclass
class WopiWebAppProperties(ClientValue):

    App: Optional[str] = None
    BootstrapperUrl: Optional[str] = None
    ListByAction: ClientValueCollection[WebAppUrlsByAction] = field(
        default_factory=lambda: ClientValueCollection(WebAppUrlsByAction)
    )

    @property
    def entity_type_name(self):
        return "SP.Utilities.WopiWebAppProperties"