from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AndroidLobApp(Entity):
    @property
    def package_id(self) -> Optional[str]:
        """Gets the packageId property"""
        return self.properties.get("packageId", None)

    @property
    def version_code(self) -> Optional[str]:
        """Gets the versionCode property"""
        return self.properties.get("versionCode", None)

    @property
    def version_name(self) -> Optional[str]:
        """Gets the versionName property"""
        return self.properties.get("versionName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidLobApp"
