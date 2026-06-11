from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class GridInitInfoType(ClientValue):
    ControllerId: str | None = None
    GridSerializer: str | None = None
    JsInitObj: str | None = None
