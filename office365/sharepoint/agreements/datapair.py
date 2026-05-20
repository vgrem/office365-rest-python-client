from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementDataPair(ClientValue):
    count: Optional[int] = None
    name: Optional[str] = None
