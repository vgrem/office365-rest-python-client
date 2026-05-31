from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.contenttypes.info import ContentTypeInfo
from office365.runtime.client_value import ClientValue


@dataclass
class DocumentSetContent(ClientValue):
    """Represents the default content of document set in SharePoint."""

    contentType: ContentTypeInfo | None = None
    fileName: str | None = None
    folderName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DocumentSetContent"
