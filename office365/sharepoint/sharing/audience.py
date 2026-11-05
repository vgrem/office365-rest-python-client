from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class Audience(ClientValue):
    Email: str | None = None
    Id: UUID | None = None
    Title: str | None = None
