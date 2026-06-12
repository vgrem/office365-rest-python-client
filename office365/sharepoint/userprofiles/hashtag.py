from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class Hashtag(ClientValue):
    Actor: str | None = None
    Application: str | None = None
    Label: str | None = None
    Timestamp: datetime | None = field(default_factory=lambda: datetime.min)
