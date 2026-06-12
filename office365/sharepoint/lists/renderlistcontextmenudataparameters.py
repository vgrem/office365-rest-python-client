from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RenderListContextMenuDataParameters(ClientValue):
    CascDelWarnMessage: str | None = None
    CustomAction: str | None = None
    Field: str | None = None
    ID: str | None = None
    InplaceFullListSearch: str | None = None
    InplaceSearchQuery: str | None = None
    IsCSR: str | None = None
    IsXslView: str | None = None
    ItemId: str | None = None
    ListViewPageUrl: str | None = None
    OverrideScope: str | None = None
    RootFolder: str | None = None
    View: str | None = None
    ViewCount: str | None = None
