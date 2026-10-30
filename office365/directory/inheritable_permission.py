from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import key, odata

if TYPE_CHECKING:
    from office365.directory.applications.inheritable_scopes import InheritableScopes


@key("resourceAppId")
class InheritablePermission(Entity):
    @odata(name="inheritableScopes")
    @property
    def inheritable_scopes(self) -> InheritableScopes:
        """Gets the inheritableScopes property"""
        from office365.directory.applications.inheritable_scopes import (
            InheritableScopes,
        )

        return self.properties.get("inheritableScopes", InheritableScopes())

    @odata(name="resourceAppId")
    @property
    def resource_app_id(self) -> Optional[str]:
        """Gets the resourceAppId property"""
        return self.properties.get("resourceAppId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritablePermission"
