from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.contentformat import ContentFormat


class FormattedContent(ClientValue):
    content: str | None = None
    format: ContentFormat = ContentFormat.text

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FormattedContent"
