from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WindowsMobileMSI(Entity):
    @odata(name="commandLine")
    @property
    def command_line(self) -> Optional[str]:
        """Gets the commandLine property"""
        return self.properties.get("commandLine", None)

    @odata(name="ignoreVersionDetection")
    @property
    def ignore_version_detection(self) -> Optional[bool]:
        """Gets the ignoreVersionDetection property"""
        return self.properties.get("ignoreVersionDetection", None)

    @odata(name="productCode")
    @property
    def product_code(self) -> Optional[str]:
        """Gets the productCode property"""
        return self.properties.get("productCode", None)

    @odata(name="productVersion")
    @property
    def product_version(self) -> Optional[str]:
        """Gets the productVersion property"""
        return self.properties.get("productVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsMobileMSI"
