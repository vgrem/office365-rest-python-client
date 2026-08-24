from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.batch_convert_item_result import BatchConvertItemResult


class BatchConvertResult(ClientValue):
    results: ClientValueCollection[BatchConvertItemResult] = field(
        default_factory=lambda: ClientValueCollection(BatchConvertItemResult)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.BatchConvertResult"
