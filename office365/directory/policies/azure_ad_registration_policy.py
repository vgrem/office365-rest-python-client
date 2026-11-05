from __future__ import annotations

from dataclasses import field

from office365.intune.devices.registration_membership import DeviceRegistrationMembership
from office365.runtime.client_value import ClientValue


class AzureADRegistrationPolicy(ClientValue):
    allowedToRegister: DeviceRegistrationMembership = field(default_factory=DeviceRegistrationMembership)
    isAdminConfigurable: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AzureADRegistrationPolicy"
