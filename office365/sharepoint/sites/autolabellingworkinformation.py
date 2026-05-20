from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AutoLabellingWorkInformation(ClientValue):
    routing_hint: Optional[str] = None
    scale_unit_id: Optional[str] = None
    watermark: Optional[str] = None
    work_item_type: Optional[int] = None
