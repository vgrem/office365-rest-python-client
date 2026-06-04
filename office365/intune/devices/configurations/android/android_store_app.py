from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AndroidStoreApp(Entity):
    @property
    def app_store_url(self) -> Optional[str]:
        """Gets the appStoreUrl property"""
        return self.properties.get("appStoreUrl", None)

    @property
    def package_id(self) -> Optional[str]:
        """Gets the packageId property"""
        return self.properties.get("packageId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidStoreApp"
