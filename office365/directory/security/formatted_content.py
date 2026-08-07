from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.contentformat import ContentFormat
from office365.runtime.client_value import ClientValue


@dataclass
class FormattedContent(ClientValue):
    content: str | None = None
    format: ContentFormat = ContentFormat.text

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FormattedContent"
