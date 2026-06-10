from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AdditionalAccessStatusResponse(ClientValue):
    AdditionalAccessRequestStatus: int | None = None
    ErrorMessage: str | None = None
    RoleValue: int | None = None
    StatusCode: int | None = None
