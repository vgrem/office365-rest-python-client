from __future__ import annotations

from enum import Enum


class MdmSupportedState(Enum):
    unknown = "0"
    supported = "1"
    unsupported = "2"
    deprecated = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MdmSupportedState"
