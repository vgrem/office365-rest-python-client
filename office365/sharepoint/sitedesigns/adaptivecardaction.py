from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AdaptiveCardAction(ClientValue):
    title: Optional[str] = None
    isPrimary: bool | None = None
