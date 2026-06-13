from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class MultiGeoCopyParameters(ClientValue):
    binaryPayload: bytes | None = None
    jobId: UUID | None = None
    userId: int | None = None
