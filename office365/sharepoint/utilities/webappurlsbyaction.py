from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.utilities.webappexturlpair import WebAppExtUrlPair


@value
class WebAppUrlsByAction(ClientValue):
    Action: Optional[str] = None
    UrlsByExt: ClientValueCollection[WebAppExtUrlPair] = field(
        default_factory=lambda: ClientValueCollection(WebAppExtUrlPair)
    )

    @property
    def entity_type_name(self):
        return "SP.Utilities.WebAppUrlsByAction"
