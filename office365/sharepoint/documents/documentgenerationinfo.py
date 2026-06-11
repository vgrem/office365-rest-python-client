from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.contentassemblyformanswer import ContentAssemblyFormAnswer
from office365.sharepoint.documents.location import DocumentLocation


@dataclass
class DocumentGenerationInfo(ClientValue):
    DocumentLocation: DocumentLocation = field(default_factory=DocumentLocation)
    AllowEncryptedTemplate: bool | None = None
    ConditionalFieldsToBeDeleted: StringCollection = field(default_factory=StringCollection)
    ContentAssemblyFormAnswers: ClientValueCollection[ContentAssemblyFormAnswer] = field(
        default_factory=lambda: ClientValueCollection(ContentAssemblyFormAnswer)
    )
    CopyFieldsFromExistingDocument: bool | None = None
    FileName: str | None = None
    FolderUrl: str | None = None
    Format: int | None = None
    IsAssociatedWithDocForms: bool | None = None
    IsTempFile: bool | None = None
    SkipValidationForHiddenFields: bool | None = None
    TempFileUrl: str | None = None
    UpdateFolderPermissions: bool | None = None
