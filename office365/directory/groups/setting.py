from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.setting_value import SettingValue


class GroupSetting(Entity):
    """Group settings control behaviors such as blocked word lists for group display names or whether guest users are
    allowed to be group owners."""

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="templateId")
    @property
    def template_id(self) -> Optional[str]:
        """Gets the templateId property"""
        return self.properties.get("templateId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupSetting"

    @odata(name="values")
    @property
    def values(self) -> ClientValueCollection[SettingValue]:
        """Gets the values property"""
        from office365.runtime.types.setting_value import SettingValue

        return self.properties.get("values", ClientValueCollection[SettingValue](SettingValue))
