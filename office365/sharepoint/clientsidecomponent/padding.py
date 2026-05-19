from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Padding(ClientValue):
    bottom: str | None = None
    left: str | None = None
    right: str | None = None
    top: str | None = None
