from __future__ import annotations

from office365.directory.identitygovernance.content_base import ContentBase
from office365.runtime.types.value import value


@value
class TextContent(ContentBase):
    data: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TextContent"
