from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.security.datasecurity.process_content_response import ProcessContentResponse


class ProcessContentResponses(ClientValue):
    requestId: str | None = None
    results: ProcessContentResponse = field(default_factory=ProcessContentResponse)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessContentResponses"
