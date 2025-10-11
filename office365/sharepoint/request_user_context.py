from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.principal.users.user import User


class RequestUserContext(Entity):
    """The class that represents the user context for the present request. Typically found under /_api/me"""

    @property
    def current(self) -> RequestUserContext:
        """Gets the SP.RequestUserContext for the current request."""
        return self.properties.get(
            "Current",
            RequestUserContext(self.context, ResourcePath("Current", self.resource_path)),
        )

    @property
    def user(self) -> User:
        """The SP.User object for the current request."""
        from office365.sharepoint.principal.users.user import User

        return self.properties.get("User", User(self.context, ResourcePath("User", self.resource_path)))
