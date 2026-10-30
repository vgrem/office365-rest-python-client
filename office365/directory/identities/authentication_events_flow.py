from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.conditions.conditions import (
        AuthenticationConditions,
    )


class AuthenticationEventsFlow(Entity):
    @odata(name="conditions")
    @property
    def conditions(self) -> AuthenticationConditions:
        """Gets the conditions property"""
        from office365.directory.authentication.conditions.conditions import (
            AuthenticationConditions,
        )

        return self.properties.get("conditions", AuthenticationConditions())

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationEventsFlow"
