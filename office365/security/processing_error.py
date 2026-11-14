from __future__ import annotations

from office365.security.contentprocessingerrortype import ContentProcessingErrorType
from office365.security.datasecurity.classification_error import ClassificationError


class ProcessingError(ClassificationError):
    errorType: ContentProcessingErrorType = ContentProcessingErrorType.transient

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessingError"
