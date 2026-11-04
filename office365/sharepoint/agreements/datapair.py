from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AgreementDataPair(ClientValue):
    Count: int | None = None
    Name: str | None = None
