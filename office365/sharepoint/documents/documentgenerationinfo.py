from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.contentassemblyformanswer import (
    ContentAssemblyFormAnswer,
)
from office365.sharepoint.documents.location import DocumentLocation


@dataclass
class DocumentGenerationInfo(ClientValue):
    conditional_fields_to_be_deleted: StringCollection = field(default_factory=StringCollection)
    content_assembly_form_answers: ClientValueCollection[ContentAssemblyFormAnswer] = field(
        default_factory=lambda: ClientValueCollection(ContentAssemblyFormAnswer)
    )
    copy_fields_from_existing_document: Optional[bool] = None
    file_name: Optional[str] = None
    folder_url: Optional[str] = None
    format: Optional[int] = None
    is_temp_file: Optional[bool] = None
    temp_file_url: Optional[str] = None
    update_folder_permissions: Optional[bool] = None
    DocumentLocation: DocumentLocation = field(default_factory=DocumentLocation)
