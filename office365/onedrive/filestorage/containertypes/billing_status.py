"""Billing status of a SharePoint Embedded container type.

``valid`` — billing is active and the container type can be used.
``warning`` — billing issue detected (e.g., approaching expiry).
``expired`` — the trial period or billing has expired.

https://learn.microsoft.com/en-us/graph/api/resources/filestoragecontainertype
"""

from __future__ import annotations

from enum import Enum


class FileStorageContainerBillingStatus(str, Enum):
    Valid = "valid"
    Warning = "warning"
    Expired = "expired"
    UnknownFutureValue = "unknownFutureValue"
    invalid = "0"
    valid = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerBillingStatus"
