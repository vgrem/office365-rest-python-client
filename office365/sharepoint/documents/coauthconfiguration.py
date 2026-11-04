from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CoAuthConfiguration(ClientValue):
    SourceSessionId: UUID | None = None
    UpdateDate: datetime | None = field(default_factory=lambda: datetime.min)
    UpdateReason: int | None = None
