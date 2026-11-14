from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class DeviceLocalCredential(ClientValue):
    accountName: str | None = None
    accountSid: str | None = None
    backupDateTime: datetime | None = None
    passwordBase64: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceLocalCredential"
