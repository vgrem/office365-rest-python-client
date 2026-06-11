from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class AppViewCreationInfo(ClientValue):
    AppId: UUID | None = None
    IsPrivate: bool | None = None
    Title: str | None = None
