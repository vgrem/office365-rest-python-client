from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Audience(ClientValue):
    Email: str | None = None
    Id: UUID | None = None
    Title: str | None = None
