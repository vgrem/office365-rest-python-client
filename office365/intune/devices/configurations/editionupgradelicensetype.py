from enum import Enum


class EditionUpgradeLicenseType(Enum):
    productKey = "0"
    licenseFile = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EditionUpgradeLicenseType"
