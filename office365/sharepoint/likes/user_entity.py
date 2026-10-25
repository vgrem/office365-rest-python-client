from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class UserEntity(Entity):
    """Represents a single like within a likedBy set of the list item."""

    @odata(name="creationDate")
    @property
    def creation_date(self) -> Optional[str]:
        """The Datetime of the like."""
        return self.properties.get("creationDate", None)

    @odata(name="email")
    @property
    def email(self) -> Optional[str]:
        """The email of the user who liked the item."""
        return self.properties.get("email", None)

    @odata(name="id")
    @property
    def id_(self) -> Optional[int]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="loginName")
    @property
    def login_name(self) -> Optional[str]:
        """Gets the loginName property"""
        return self.properties.get("loginName", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Likes.UserEntity"

    @odata(name="id")
    @property
    def id(self) -> Optional[int]:
        """Gets the id property"""
        return self.properties.get("id", None)
