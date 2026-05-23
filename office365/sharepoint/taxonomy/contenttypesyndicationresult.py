from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContentTypeSyndicationResult(ClientValue):
    FailedContentTypeErrors: StringCollection = field(default_factory=StringCollection)
    FailedContentTypeIDs: StringCollection = field(default_factory=StringCollection)
    FailedReason: int | None = None
    IsPassed: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Taxonomy.ContentTypeSync.ContentTypeSyndicationResult"
