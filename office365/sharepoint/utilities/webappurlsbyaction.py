from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.webappexturlpair import WebAppExtUrlPair


@dataclass
class WebAppUrlsByAction(ClientValue):

    Action: Optional[str] = None
    UrlsByExt: ClientValueCollection[WebAppExtUrlPair] = ClientValueCollection(WebAppExtUrlPair)

    @property
    def entity_type_name(self):
        return "SP.Utilities.WebAppUrlsByAction"