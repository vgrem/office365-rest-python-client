from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.datasecurity.process_content_request import ProcessContentRequest
from office365.runtime.client_value import ClientValue


@dataclass
class ProcessContentBatchRequest(ClientValue):
    contentToProcess: ProcessContentRequest = field(default_factory=ProcessContentRequest)
    requestId: str | None = None
    userId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessContentBatchRequest"
