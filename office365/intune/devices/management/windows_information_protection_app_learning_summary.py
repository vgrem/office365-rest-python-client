from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.informationprotection.applicationtype import ApplicationType
from office365.runtime.types.odata_property import odata


class WindowsInformationProtectionAppLearningSummary(Entity):
    @odata(name="applicationName")
    @property
    def application_name(self) -> Optional[str]:
        """Gets the applicationName property"""
        return self.properties.get("applicationName", None)

    @odata(name="applicationType")
    @property
    def application_type(self) -> ApplicationType:
        """Gets the applicationType property"""
        return self.properties.get("applicationType", ApplicationType.universal)

    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionAppLearningSummary"
