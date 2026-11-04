from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UploadDocumentInfo(ClientValue):
    AgreementLibraryId: str | None = None
    FileItemId: int | None = None
    FileName: str | None = None
    FileServerRedirectedEmbedUrl: str | None = None
    FileServerRelativeUrl: str | None = None
    FileUniqueId: str | None = None
    FolderItemId: int | None = None
    FolderServerRelativeUrl: str | None = None
