from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementCountryResponse(ClientValue):
    CountryKey: str | None = None
    DisplayName: str | None = None
