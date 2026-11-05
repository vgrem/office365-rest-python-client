from __future__ import annotations

from office365.runtime.client_value import ClientValue


class PrintDocumentUploadProperties(ClientValue):
    contentType: str | None = None
    documentName: str | None = None
    size: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintDocumentUploadProperties"
