from typing import Optional

from office365.runtime.client_value import ClientValue


class SensitivityLabelInformation(ClientValue):
    def __init__(
        self,
        color: Optional[str] = None,
        display_name: Optional[str] = None,
        has_irm_protection: Optional[bool] = None,
        id_: Optional[str] = None,
        sensitivity_label_protection_type: Optional[str] = None,
        tooltip: Optional[str] = None,
    ):
        self.color = color
        self.displayName = display_name
        self.hasIRMProtection = has_irm_protection
        self.id = id_
        self.sensitivityLabelProtectionType = sensitivity_label_protection_type
        self.tooltip = tooltip

    @property
    def entity_type_name(self):
        return "SP.Sharing.SensitivityLabelInformation"
