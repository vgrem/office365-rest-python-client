from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class IosiPadOSWebClip(Entity):
    @odata(name="appUrl")
    @property
    def app_url(self) -> Optional[str]:
        """Gets the appUrl property"""
        return self.properties.get("appUrl", None)

    @odata(name="useManagedBrowser")
    @property
    def use_managed_browser(self) -> Optional[bool]:
        """Gets the useManagedBrowser property"""
        return self.properties.get("useManagedBrowser", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosiPadOSWebClip"
