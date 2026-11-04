from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CAFieldValue(ClientValue):
    DataType: str | None = None
    Id: str | None = None
    Name: str | None = None
    Value: str | None = None
