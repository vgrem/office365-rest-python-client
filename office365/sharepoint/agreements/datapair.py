from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AgreementDataPair(ClientValue):
    Count: int | None = None
    Name: str | None = None
