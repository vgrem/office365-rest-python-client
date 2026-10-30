from __future__ import annotations

from typing import Optional

from office365.directory.groups.setting_template_value import SettingTemplateValue
from office365.directory.objects.object import DirectoryObject
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class GroupSettingTemplate(DirectoryObject):
    """Group setting templates represent system-defined settings available to the tenant. Group settings can be
    created based on the available groupSettingTemplates, and values changed from their preset defaults.
    """

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="values")
    @property
    def values(self) -> ClientValueCollection[SettingTemplateValue]:
        """Gets the values property"""
        return self.properties.get("values", ClientValueCollection[SettingTemplateValue](SettingTemplateValue))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupSettingTemplate"
