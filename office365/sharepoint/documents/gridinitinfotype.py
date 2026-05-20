from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GridInitInfoType(ClientValue):
    controller_id: Optional[str] = None
    grid_serializer: Optional[str] = None
    js_init_obj: Optional[str] = None
