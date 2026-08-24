from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ConversionLossItem(ClientValue):
    count: int | None = None
    detail: str | None = None
    kind: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.ConversionLossItem"
