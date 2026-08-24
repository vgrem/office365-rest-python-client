from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.conversion_loss_item import ConversionLossItem


class ConversionLossReport(ClientValue):
    isClean: bool | None = None
    items: ClientValueCollection[ConversionLossItem] = field(
        default_factory=lambda: ClientValueCollection(ConversionLossItem)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.ConversionLossReport"
