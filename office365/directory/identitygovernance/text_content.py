from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.content_base import ContentBase


@dataclass
class TextContent(ContentBase):
    data: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TextContent"
