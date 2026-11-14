from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementSettingInstance(Entity):
    @odata(name="definitionId")
    @property
    def definition_id(self) -> Optional[str]:
        """Gets the definitionId property"""
        return self.properties.get("definitionId", None)

    @odata(name="valueJson")
    @property
    def value_json(self) -> Optional[str]:
        """Gets the valueJson property"""
        return self.properties.get("valueJson", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementSettingInstance"
