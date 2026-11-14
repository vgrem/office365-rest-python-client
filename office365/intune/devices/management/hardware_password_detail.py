from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class HardwarePasswordDetail(Entity):
    @odata(name="currentPassword", readonly=True)
    @property
    def current_password(self) -> Optional[str]:
        """Gets the currentPassword property"""
        return self.properties.get("currentPassword", None)

    @odata(name="previousPasswords", readonly=True)
    @property
    def previous_passwords(self) -> StringCollection:
        """Gets the previousPasswords property"""
        return self.properties.get("previousPasswords", StringCollection())

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HardwarePasswordDetail"
