from __future__ import annotations

from dataclasses import dataclass, field

from office365.entity_collection import EntityCollection
from office365.onedrive.columns.definition import ColumnDefinition
from office365.onedrive.contenttypes.info import ContentTypeInfo
from office365.onedrive.documentsets.content import DocumentSetContent
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class DocumentSet(ClientValue):
    """Represents a document set in SharePoint."""

    welcomePageUrl: str | None = None
    allowedContentTypes: ClientValueCollection[ContentTypeInfo] = field(
        default_factory=lambda: ClientValueCollection(ContentTypeInfo)
    )
    defaultContents: ClientValueCollection[DocumentSetContent] = field(
        default_factory=lambda: ClientValueCollection(DocumentSetContent)
    )
    propagateWelcomePageChanges: bool | None = None
    shouldPrefixNameToFile: bool | None = None
    sharedColumns: EntityCollection[ColumnDefinition] | None = None
    welcomePageColumns: EntityCollection[ColumnDefinition] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DocumentSet"
