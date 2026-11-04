from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Hashtag(ClientValue):
    Actor: str | None = None
    Application: str | None = None
    Label: str | None = None
    Timestamp: datetime | None = field(default_factory=lambda: datetime.min)
