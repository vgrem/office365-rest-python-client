from __future__ import annotations

from typing import Optional

from office365.intune.devices.management.mobileapps.mobile_app import MobileApp
from office365.runtime.types.odata_property import odata


class WindowsWebApp(MobileApp):
    @odata(name="appUrl")
    @property
    def app_url(self) -> Optional[str]:
        """Gets the appUrl property"""
        return self.properties.get("appUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsWebApp"
