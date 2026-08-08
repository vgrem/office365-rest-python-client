from __future__ import annotations

from enum import Enum


class WebsiteType(Enum):
    other = "0"
    home = "1"
    work = "2"
    blog = "3"
    profile = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebsiteType"
