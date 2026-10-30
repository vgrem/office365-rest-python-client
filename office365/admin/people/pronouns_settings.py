from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class PronounsSettings(Entity):
    @odata(name="isEnabledInOrganization")
    @property
    def is_enabled_in_organization(self) -> Optional[bool]:
        """Gets the isEnabledInOrganization property"""
        return self.properties.get("isEnabledInOrganization", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PronounsSettings"
