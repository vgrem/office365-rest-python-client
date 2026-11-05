from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class AccessRequestResponse(ClientValue):
    result: Optional[bool] = None
    requestedObjectId: UUID | None = None
