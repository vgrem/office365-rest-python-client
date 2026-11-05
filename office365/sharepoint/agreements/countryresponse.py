from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AgreementCountryResponse(ClientValue):
    CountryKey: str | None = None
    DisplayName: str | None = None
