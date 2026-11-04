from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AgreementCountryResponse(ClientValue):
    CountryKey: str | None = None
    DisplayName: str | None = None
