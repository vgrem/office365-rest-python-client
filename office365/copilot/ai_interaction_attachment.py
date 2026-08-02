from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AiInteractionAttachment(ClientValue):
    attachmentId: str | None = None
    content: str | None = None
    contentType: str | None = None
    contentUrl: str | None = None
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionAttachment"
