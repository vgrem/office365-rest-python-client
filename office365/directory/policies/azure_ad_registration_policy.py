from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.registration_membership import DeviceRegistrationMembership
from office365.runtime.client_value import ClientValue


@dataclass
class AzureADRegistrationPolicy(ClientValue):
    allowedToRegister: DeviceRegistrationMembership = field(default_factory=DeviceRegistrationMembership)
    isAdminConfigurable: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AzureADRegistrationPolicy"
