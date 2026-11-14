from __future__ import annotations

from office365.security.alerts.evidence import AlertEvidence
from office365.security.filehashalgorithm import FileHashAlgorithm


class FileHashEvidence(AlertEvidence):
    algorithm: FileHashAlgorithm = FileHashAlgorithm.unknown
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileHashEvidence"
