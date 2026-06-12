from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class VisualizationAppInfo(ClientValue):
    DesignUri: str | None = None
    Id: UUID | None = None
    RuntimeUri: str | None = None
