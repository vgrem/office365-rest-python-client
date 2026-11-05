from __future__ import annotations

from office365.runtime.client_value import ClientValue


class RgbColor(ClientValue):
    b: int | None = None
    g: int | None = None
    r: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RgbColor"
