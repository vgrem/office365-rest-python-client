from __future__ import annotations

from dataclasses import field

from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EmergencyCallerInfo(ClientValue):
    displayName: str | None = None
    location: Location = field(default_factory=Location)
    phoneNumber: str | None = None
    tenantId: str | None = None
    upn: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmergencyCallerInfo"
