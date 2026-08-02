from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ChangeNotificationEncryptedContent(ClientValue):
    data: str | None = None
    dataKey: str | None = None
    dataSignature: str | None = None
    encryptionCertificateId: str | None = None
    encryptionCertificateThumbprint: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChangeNotificationEncryptedContent"
