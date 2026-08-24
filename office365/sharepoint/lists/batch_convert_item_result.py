from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.conversion_loss_report import ConversionLossReport


class BatchConvertItemResult(ClientValue):
    errorCode: str | None = None
    errorMessage: str | None = None
    lossy: ConversionLossReport = field(default_factory=ConversionLossReport)
    sourceItemId: int | None = None
    succeeded: bool | None = None
    viewerUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.BatchConvertItemResult"
