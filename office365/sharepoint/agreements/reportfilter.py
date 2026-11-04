from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AgreementReportFilter(ClientValue):
    Category: str | None = None
    FirstParty: str | None = None
    Language: str | None = None
    Location: str | None = None
    Owner: str | None = None
    SecondParty: str | None = None
    State: str | None = None
