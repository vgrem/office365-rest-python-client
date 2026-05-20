from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementReportFilter(ClientValue):
    category: Optional[str] = None
    first_party: Optional[str] = None
    language: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    second_party: Optional[str] = None
    state: Optional[str] = None
