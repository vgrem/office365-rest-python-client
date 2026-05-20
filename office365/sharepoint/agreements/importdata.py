from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementImportData(ClientValue):
    extraction_pending: Optional[int] = None
    user_confirmation_pending: Optional[int] = None
