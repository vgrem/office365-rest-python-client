from __future__ import annotations

from office365.runtime.client_value import ClientValue


class GridInitInfoType(ClientValue):
    ControllerId: str | None = None
    GridSerializer: str | None = None
    JsInitObj: str | None = None
