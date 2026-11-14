from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.process_content_metadata_base import ProcessContentMetadataBase
from office365.security.datasecurity.custom_metadata_dictionary import CustomMetadataDictionary


class ProcessFileMetadata(ProcessContentMetadataBase):
    customProperties: CustomMetadataDictionary = field(default_factory=CustomMetadataDictionary)
    ownerId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessFileMetadata"
