from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPImageItem(ClientValue):
    Name: str | None = None
    ServerRelativeUrl: str | None = None
    UniqueId: UUID | None = None
