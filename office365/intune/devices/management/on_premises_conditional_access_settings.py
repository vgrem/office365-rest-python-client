from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata


class OnPremisesConditionalAccessSettings(Entity):
    @odata(name="enabled")
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the enabled property"""
        return self.properties.get("enabled", None)

    @odata(name="excludedGroups")
    @property
    def excluded_groups(self) -> GuidCollection:
        """Gets the excludedGroups property"""
        return self.properties.get("excludedGroups", GuidCollection())

    @odata(name="includedGroups")
    @property
    def included_groups(self) -> GuidCollection:
        """Gets the includedGroups property"""
        return self.properties.get("includedGroups", GuidCollection())

    @odata(name="overrideDefaultRule")
    @property
    def override_default_rule(self) -> Optional[bool]:
        """Gets the overrideDefaultRule property"""
        return self.properties.get("overrideDefaultRule", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesConditionalAccessSettings"
