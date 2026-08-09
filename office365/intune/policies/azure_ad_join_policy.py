from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.registration_membership import DeviceRegistrationMembership
from office365.intune.policies.local_admin_settings import LocalAdminSettings
from office365.runtime.client_value import ClientValue


@dataclass
class AzureADJoinPolicy(ClientValue):
    allowedToJoin: DeviceRegistrationMembership = field(default_factory=DeviceRegistrationMembership)
    isAdminConfigurable: bool | None = None
    localAdmins: LocalAdminSettings = field(default_factory=LocalAdminSettings)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AzureADJoinPolicy"
