from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CardElement(ClientValue):
    id: Optional[str] = None
    isVisible: Optional[bool] = None
    separator: Optional[bool] = None
    spacing: Optional[str] = None
    type: Optional[str] = None
