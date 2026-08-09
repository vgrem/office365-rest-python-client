from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.registration_membership import DeviceRegistrationMembership
from office365.runtime.client_value import ClientValue


@dataclass
class LocalAdminSettings(ClientValue):
    enableGlobalAdmins: bool | None = None
    registeringUsers: DeviceRegistrationMembership = field(default_factory=DeviceRegistrationMembership)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LocalAdminSettings"
