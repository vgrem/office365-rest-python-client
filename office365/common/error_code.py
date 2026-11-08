from __future__ import annotations

from enum import Enum


class ErrorCode(Enum):
    noError = "0"
    unauthorized = "1"
    notFound = "2"
    deleted = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ErrorCode"
