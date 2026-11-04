from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PopularTenantQuery(ClientValue):
    AlwaysSuggest: bool | None = None
    ClickCount: int | None = None
    LCID: int | None = None
    QueryCount: int | None = None
    QueryText: str | None = None
    SiteId: str | None = None
    SourceId: str | None = None
    WebId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.PopularTenantQuery"
