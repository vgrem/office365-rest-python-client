from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementCountryResponse(ClientValue):
    country_key: Optional[str] = None
    display_name: Optional[str] = None
