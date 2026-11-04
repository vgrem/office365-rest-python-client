from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TextBlock(ClientValue):
    color: Optional[str] = None
    size: Optional[str] = None
    text: Optional[str] = None
    weight: Optional[str] = None
    wrap: Optional[bool] = None
    horizontalAlignment: str | None = None
