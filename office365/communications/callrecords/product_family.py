from __future__ import annotations

from enum import Enum


class ProductFamily(Enum):
    unknown = "0"
    teams = "1"
    skypeForBusiness = "2"
    lync = "3"
    unknownFutureValue = "4"
    azureCommunicationServices = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.ProductFamily"
