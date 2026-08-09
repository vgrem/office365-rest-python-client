from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.contentprocessingerrortype import ContentProcessingErrorType
from office365.runtime.client_value import ClientValue


@dataclass
class ProcessingError(ClientValue):
    errorType: ContentProcessingErrorType = ContentProcessingErrorType.transient

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessingError"
