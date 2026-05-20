from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class Audience(ClientValue):
    email: str | None = None
    id: UUID | None = None
    title: str | None = None
