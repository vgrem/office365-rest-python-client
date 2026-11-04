from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WindowsInformationProtectionDataRecoveryCertificate(ClientValue):
    certificate: bytes | None = None
    description: str | None = None
    expirationDateTime: datetime | None = None
    subjectName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionDataRecoveryCertificate"
