from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.users.user import User


class EngagementRoleMember(Entity):
    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="userId", readonly=True)
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @odata(name="user", navigation=True)
    @property
    def user(self) -> User:
        """Gets the user property"""
        from office365.directory.users.user import User

        return self.properties.get("user", User(self.context, ResourcePath("user", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EngagementRoleMember"
