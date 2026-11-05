from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AiInteractionLink(ClientValue):
    displayName: str | None = None
    linkType: str | None = None
    linkUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionLink"
