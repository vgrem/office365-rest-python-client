from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class SmartWikiMetadataUpdateParameters(ClientValue):
    description: str | None = None
    sources: StringCollection = field(default_factory=StringCollection)
    tags: StringCollection = field(default_factory=StringCollection)
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SmartWikiLibrary.SmartWikiMetadataUpdateParameters"
