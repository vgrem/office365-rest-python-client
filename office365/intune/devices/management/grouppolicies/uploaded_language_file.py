from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class GroupPolicyUploadedLanguageFile(ClientValue):
    content: bytes | None = None
    fileName: str | None = None
    id: str | None = None
    languageCode: str | None = None
    lastModifiedDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyUploadedLanguageFile"
