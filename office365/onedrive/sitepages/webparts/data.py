from __future__ import annotations

from dataclasses import field

from office365.onedrive.server_processed_content import ServerProcessedContent
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WebPartData(ClientValue):
    dataVersion: str | None = None
    description: str | None = None
    properties: dict | None = None
    serverProcessedContent: ServerProcessedContent = field(default_factory=ServerProcessedContent)
    title: str | None = None
    ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebPartData"
