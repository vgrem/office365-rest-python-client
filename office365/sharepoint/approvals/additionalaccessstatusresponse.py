from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AdditionalAccessStatusResponse(ClientValue):
    AdditionalAccessRequestStatus: int | None = None
    ErrorMessage: str | None = None
    RoleValue: int | None = None
    StatusCode: int | None = None
