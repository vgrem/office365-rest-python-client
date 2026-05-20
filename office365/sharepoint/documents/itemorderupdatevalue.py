from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ItemOrderUpdateValue(ClientValue):
    has_exception: Optional[bool] = None
    item_id: Optional[int] = None
    updated_order: Optional[float] = None
