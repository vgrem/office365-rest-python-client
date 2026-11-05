from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ItemOrderUpdateValue(ClientValue):
    HasException: bool | None = None
    ItemId: int | None = None
    UpdatedOrder: float | None = None
