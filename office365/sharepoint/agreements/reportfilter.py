from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementReportFilter(ClientValue):
    Category: str | None = None
    FirstParty: str | None = None
    Language: str | None = None
    Location: str | None = None
    Owner: str | None = None
    SecondParty: str | None = None
    State: str | None = None
