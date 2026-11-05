from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BatchConvertClassicWikiPageInput(ClientValue):
    order: float | None = None
    sourceItemId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.BatchConvertClassicWikiPageInput"
