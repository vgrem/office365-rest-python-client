from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPResourceEntry(ClientValue):
    LCID: int | None = None
    Value: str | None = None
