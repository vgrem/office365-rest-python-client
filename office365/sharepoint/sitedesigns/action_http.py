from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.header import Header


class ActionHttp(ClientValue):
    body: str | None = None
    headers: ClientValueCollection[Header] = field(default_factory=lambda: ClientValueCollection(Header))
    method: str | None = None
    url: str | None = None
