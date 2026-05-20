from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SensitivityLabelInformation(ClientValue):
    color: str | None = None
    displayName: str | None = None
    hasIRMProtection: bool | None = None
    id: str | None = None
    sensitivityLabelProtectionType: str | None = None
    tooltip: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SensitivityLabelInformation"
