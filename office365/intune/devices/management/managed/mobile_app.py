from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.mobileapps.mobile_app_identifier import MobileAppIdentifier
from office365.runtime.types.odata_property import odata


class ManagedMobileApp(Entity):
    @odata(name="mobileAppIdentifier")
    @property
    def mobile_app_identifier(self) -> MobileAppIdentifier:
        """Gets the mobileAppIdentifier property"""
        return self.properties.get("mobileAppIdentifier", MobileAppIdentifier())

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedMobileApp"
