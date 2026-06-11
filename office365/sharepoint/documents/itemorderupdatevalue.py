from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ItemOrderUpdateValue(ClientValue):
    HasException: bool | None = None
    ItemId: int | None = None
    UpdatedOrder: float | None = None
