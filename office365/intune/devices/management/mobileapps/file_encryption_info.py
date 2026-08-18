from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileEncryptionInfo(ClientValue):
    encryptionKey: bytes | None = None
    fileDigest: bytes | None = None
    fileDigestAlgorithm: str | None = None
    initializationVector: bytes | None = None
    mac: bytes | None = None
    macKey: bytes | None = None
    profileIdentifier: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileEncryptionInfo"
