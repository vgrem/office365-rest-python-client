from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateAgreementStatePayload(ClientValue):
    agreement_url: Optional[str] = None
    current_state: Optional[int] = None
    next_state: Optional[int] = None
