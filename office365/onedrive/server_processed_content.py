from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.meta_data_key_string_pair import MetaDataKeyStringPair
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ServerProcessedContent(ClientValue):
    htmlStrings: ClientValueCollection[MetaDataKeyStringPair] = field(
        default_factory=lambda: ClientValueCollection(MetaDataKeyStringPair)
    )
    imageSources: ClientValueCollection[MetaDataKeyStringPair] = field(
        default_factory=lambda: ClientValueCollection(MetaDataKeyStringPair)
    )
    links: ClientValueCollection[MetaDataKeyStringPair] = field(
        default_factory=lambda: ClientValueCollection(MetaDataKeyStringPair)
    )
    searchablePlainTexts: ClientValueCollection[MetaDataKeyStringPair] = field(
        default_factory=lambda: ClientValueCollection(MetaDataKeyStringPair)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServerProcessedContent"
