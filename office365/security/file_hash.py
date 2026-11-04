from __future__ import annotations

from office365.onedrive.files.hashtype import FileHashType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.filehashalgorithm import FileHashAlgorithm


@value
class FileHash(ClientValue):
    algorithm: FileHashAlgorithm = FileHashAlgorithm.unknown
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FileHash"

    hashType: FileHashType = FileHashType.unknown

    hashValue: str | None = None
