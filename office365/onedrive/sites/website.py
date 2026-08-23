from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.sites.website_type import WebsiteType
from office365.runtime.client_value import ClientValue


@dataclass
class Website(ClientValue):
    address: str | None = None
    displayName: str | None = None
    type: WebsiteType = WebsiteType.other

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Website"
