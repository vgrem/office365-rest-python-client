from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SearchObjectOwnerResult(ClientValue):
    """This object contains the search object owner in the result."""

    SiteCollectionId: str | None = None
    SiteId: str | None = None
    TenantId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchObjectOwnerResult"
