from office365.runtime.client_value import ClientValue


class SensitivityLabelInformation(ClientValue):
    def __init__(
        self,
        color: str = None,
        display_name: str = None,
        has_irm_protection: bool = None,
        id_: str = None,
        sensitivity_label_protection_type: str = None,
        tooltip: str = None,
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
