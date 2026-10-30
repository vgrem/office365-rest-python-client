from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WindowsInformationProtectionAppLockerFile(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="file")
    @property
    def file(self) -> Optional[bytes]:
        """Gets the file property"""
        return self.properties.get("file", None)

    @odata(name="fileHash")
    @property
    def file_hash(self) -> Optional[str]:
        """Gets the fileHash property"""
        return self.properties.get("fileHash", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsInformationProtectionAppLockerFile"
