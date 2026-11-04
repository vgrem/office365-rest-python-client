from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MultiGeoCopyParameters(ClientValue):
    binaryPayload: bytes | None = None
    jobId: UUID | None = None
    userId: int | None = None
