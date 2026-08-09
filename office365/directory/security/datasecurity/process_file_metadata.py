from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.datasecurity.custom_metadata_dictionary import CustomMetadataDictionary
from office365.runtime.client_value import ClientValue


@dataclass
class ProcessFileMetadata(ClientValue):
    customProperties: CustomMetadataDictionary = field(default_factory=CustomMetadataDictionary)
    ownerId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessFileMetadata"
