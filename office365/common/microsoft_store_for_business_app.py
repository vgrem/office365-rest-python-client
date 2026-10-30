from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.microsoftstoreforbusinesslicensetype import (
        MicrosoftStoreForBusinessLicenseType,
    )


class MicrosoftStoreForBusinessApp(Entity):
    @odata(name="licenseType")
    @property
    def license_type(self) -> MicrosoftStoreForBusinessLicenseType:
        """Gets the licenseType property"""
        from office365.intune.devices.compliance.microsoftstoreforbusinesslicensetype import (
            MicrosoftStoreForBusinessLicenseType,
        )

        return self.properties.get("licenseType", MicrosoftStoreForBusinessLicenseType.offline)

    @odata(name="packageIdentityName")
    @property
    def package_identity_name(self) -> Optional[str]:
        """Gets the packageIdentityName property"""
        return self.properties.get("packageIdentityName", None)

    @odata(name="productKey")
    @property
    def product_key(self) -> Optional[str]:
        """Gets the productKey property"""
        return self.properties.get("productKey", None)

    @odata(name="totalLicenseCount")
    @property
    def total_license_count(self) -> Optional[int]:
        """Gets the totalLicenseCount property"""
        return self.properties.get("totalLicenseCount", None)

    @odata(name="usedLicenseCount")
    @property
    def used_license_count(self) -> Optional[int]:
        """Gets the usedLicenseCount property"""
        return self.properties.get("usedLicenseCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftStoreForBusinessApp"
