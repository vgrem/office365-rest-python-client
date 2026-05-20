from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementSearchParameters(ClientValue):
    agreement_number: Optional[str] = None
    category: Optional[str] = None
    owner: Optional[str] = None
    row_limit: Optional[int] = None
    start_row: Optional[int] = None
    state: Optional[str] = None
