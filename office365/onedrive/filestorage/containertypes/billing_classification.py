"""Billing classification for a SharePoint Embedded container type.

``trial`` — free, expires after 30 days, limited to 5 containers.
``standard`` — production use, requires an Azure subscription and billing profile.
``directToCustomer`` — passthrough billing, charged directly to the consuming tenant.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from enum import Enum


class FileStorageContainerBillingClassification(str, Enum):
    Trial = "trial"
    Standard = "standard"
    DirectToCustomer = "directToCustomer"
    UnknownFutureValue = "unknownFutureValue"
    standard = "0"
    trial = "1"
    directToCustomer = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerBillingClassification"
