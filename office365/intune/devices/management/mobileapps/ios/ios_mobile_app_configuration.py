from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class IosMobileAppConfiguration(Entity):
    @property
    def encoded_setting_xml(self) -> Optional[bytes]:
        """Gets the encodedSettingXml property"""
        return self.properties.get("encodedSettingXml", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosMobileAppConfiguration"
