from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContentTypeSyndicationResult(ClientValue):
    FailedContentTypeErrors: StringCollection = field(default_factory=StringCollection)
    FailedContentTypeIDs: StringCollection = field(default_factory=StringCollection)
    FailedReason: Optional[int] = None
    IsPassed: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.ContentTypeSync.ContentTypeSyndicationResult"
