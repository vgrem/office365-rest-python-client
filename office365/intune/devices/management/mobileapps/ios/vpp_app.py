from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.mobileapps.ios.ios_device_type import IosDeviceType
from office365.intune.devices.management.mobileapps.vpp_licensing_type import VppLicensingType
from office365.intune.devices.management.vpptokens.accounttype import VppTokenAccountType
from office365.runtime.types.odata_property import odata


class IosVppApp(Entity):
    @odata(name="applicableDeviceType")
    @property
    def applicable_device_type(self) -> IosDeviceType:
        """Gets the applicableDeviceType property"""
        return self.properties.get("applicableDeviceType", IosDeviceType())

    @odata(name="appStoreUrl")
    @property
    def app_store_url(self) -> Optional[str]:
        """Gets the appStoreUrl property"""
        return self.properties.get("appStoreUrl", None)

    @odata(name="bundleId")
    @property
    def bundle_id(self) -> Optional[str]:
        """Gets the bundleId property"""
        return self.properties.get("bundleId", None)

    @odata(name="licensingType")
    @property
    def licensing_type(self) -> VppLicensingType:
        """Gets the licensingType property"""
        return self.properties.get("licensingType", VppLicensingType())

    @odata(name="releaseDateTime")
    @property
    def release_date_time(self) -> Optional[datetime]:
        """Gets the releaseDateTime property"""
        return self.properties.get("releaseDateTime", datetime.min)

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

    @odata(name="vppTokenAccountType")
    @property
    def vpp_token_account_type(self) -> VppTokenAccountType:
        """Gets the vppTokenAccountType property"""
        return self.properties.get("vppTokenAccountType", VppTokenAccountType.business)

    @odata(name="vppTokenAppleId")
    @property
    def vpp_token_apple_id(self) -> Optional[str]:
        """Gets the vppTokenAppleId property"""
        return self.properties.get("vppTokenAppleId", None)

    @odata(name="vppTokenOrganizationName")
    @property
    def vpp_token_organization_name(self) -> Optional[str]:
        """Gets the vppTokenOrganizationName property"""
        return self.properties.get("vppTokenOrganizationName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosVppApp"
