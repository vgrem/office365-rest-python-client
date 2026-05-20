from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CAFieldValue(ClientValue):
    data_type: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
