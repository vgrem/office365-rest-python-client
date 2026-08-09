from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.identitygovernance.content_base import ContentBase
from office365.directory.identitygovernance.content_category import ContentCategory
from office365.runtime.client_value import ClientValue


@dataclass
class ProcessContentMetadataBase(ClientValue):
    content: ContentBase = field(default_factory=ContentBase)
    contentCategory: ContentCategory = ContentCategory.none
    correlationId: str | None = None
    createdDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    identifier: str | None = None
    isTruncated: bool | None = None
    length: int | None = None
    modifiedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    name: str | None = None
    sequenceNumber: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProcessContentMetadataBase"
