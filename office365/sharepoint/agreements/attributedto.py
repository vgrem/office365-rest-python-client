from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.approvals.user import UserDTO


@dataclass
class AgreementAttributeDTO(ClientValue):
    review_complete_date: Optional[datetime] = None
    reviewer: UserDTO = field(default_factory=UserDTO)
    review_id: Optional[str] = None
    review_start_date: Optional[datetime] = None
    state: Optional[int] = None
