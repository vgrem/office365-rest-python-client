from __future__ import annotations

from enum import Enum


class OidcResponseType(Enum):
    code = "1"
    id_token = "2"
    token = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OidcResponseType"
