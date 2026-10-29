from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import key


@key("appId")
class AuthenticationConditionApplication(Entity):
    """An object representing the application that will be triggered for an authenticationEventListener."""

    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationConditionApplication"
