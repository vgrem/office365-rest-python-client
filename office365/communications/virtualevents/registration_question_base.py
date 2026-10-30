from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class VirtualEventRegistrationQuestionBase(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isRequired")
    @property
    def is_required(self) -> Optional[bool]:
        """Gets the isRequired property"""
        return self.properties.get("isRequired", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistrationQuestionBase"
