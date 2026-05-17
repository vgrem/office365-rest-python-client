from enum import Enum


class IdentityUserFlowAttributeInputType(Enum):
    textBox = "1"
    dateTimeDropdown = "2"
    radioSingleSelect = "3"
    dropdownSingleSelect = "4"
    emailBox = "5"
    checkboxMultiSelect = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IdentityUserFlowAttributeInputType"
