from __future__ import annotations

from enum import Enum


class CustomDataProvidedResourceUploadStatus(Enum):
    active = "0"
    complete = "1"
    expired = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomDataProvidedResourceUploadStatus"
