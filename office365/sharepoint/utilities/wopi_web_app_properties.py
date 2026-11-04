from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.utilities.webappurlsbyaction import WebAppUrlsByAction


@value
class WopiWebAppProperties(ClientValue):
    App: Optional[str] = None
    BootstrapperUrl: Optional[str] = None
    ListByAction: ClientValueCollection[WebAppUrlsByAction] = field(
        default_factory=lambda: ClientValueCollection(WebAppUrlsByAction)
    )

    @property
    def entity_type_name(self):
        return "SP.Utilities.WopiWebAppProperties"
