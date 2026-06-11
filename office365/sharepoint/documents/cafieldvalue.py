from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CAFieldValue(ClientValue):
    DataType: str | None = None
    Id: str | None = None
    Name: str | None = None
    Value: str | None = None
