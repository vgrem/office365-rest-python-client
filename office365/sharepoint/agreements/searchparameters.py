from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AgreementSearchParameters(ClientValue):
    AgreementNumber: str | None = None
    Category: str | None = None
    Owner: str | None = None
    RowLimit: int | None = None
    StartRow: int | None = None
    State: str | None = None
