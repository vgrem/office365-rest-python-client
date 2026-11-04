from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class BatchConvertAssetResult(ClientValue):
    destinationUrl: str | None = None
    errorCode: str | None = None
    errorMessage: str | None = None
    mediaType: str | None = None
    sourceUrl: str | None = None
    status: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.BatchConvertAssetResult"
