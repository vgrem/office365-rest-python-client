from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AdditionalAccessStatusResponse(ClientValue):
    additional_access_request_status: Optional[int] = None
    error_message: Optional[str] = None
    role_value: Optional[int] = None
    status_code: Optional[int] = None
