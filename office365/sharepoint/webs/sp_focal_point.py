from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPFocalPoint(ClientValue):
    FocalPointX: float | None = None
    FocalPointY: float | None = None
    Hash: str | None = None
