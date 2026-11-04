from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
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
