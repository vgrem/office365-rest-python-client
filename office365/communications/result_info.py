from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ResultInfo(ClientValue):
    code: int | None = None
    message: str | None = None
    subcode: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResultInfo"
