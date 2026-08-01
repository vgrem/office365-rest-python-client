from __future__ import annotations

from dataclasses import dataclass

from office365.directory.security.filehashalgorithm import FileHashAlgorithm
from office365.runtime.client_value import ClientValue


@dataclass
class FileHashEvidence(ClientValue):
    algorithm: FileHashAlgorithm = FileHashAlgorithm.unknown
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileHashEvidence"
