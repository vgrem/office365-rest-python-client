from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.configurations.editionupgradelicensetype import EditionUpgradeLicenseType
from office365.intune.devices.configurations.windows._10.editiontype import Windows10EditionType
from office365.runtime.types.odata_property import odata


class EditionUpgradeConfiguration(Entity):
    @odata(name="license")
    @property
    def license(self) -> Optional[str]:
        """Gets the license property"""
        return self.properties.get("license", None)

    @odata(name="licenseType")
    @property
    def license_type(self) -> EditionUpgradeLicenseType:
        """Gets the licenseType property"""
        return self.properties.get("licenseType", EditionUpgradeLicenseType.productKey)

    @odata(name="productKey")
    @property
    def product_key(self) -> Optional[str]:
        """Gets the productKey property"""
        return self.properties.get("productKey", None)

    @odata(name="targetEdition")
    @property
    def target_edition(self) -> Windows10EditionType:
        """Gets the targetEdition property"""
        return self.properties.get("targetEdition", Windows10EditionType.windows10Enterprise)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EditionUpgradeConfiguration"
