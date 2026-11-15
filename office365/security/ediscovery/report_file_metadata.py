from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ReportFileMetadata(ClientValue):
    downloadUrl: str | None = None
    fileName: str | None = None
    size: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ReportFileMetadata"
