from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class ExternalUser(Entity):
    """Represents an external (guest) user in the SharePoint tenant."""

    @property
    def accepted_as(self) -> Optional[str]:
        """The email address or login name as which the user was accepted."""
        return self.properties.get("AcceptedAs", None)

    @property
    def display_name(self) -> Optional[str]:
        """The display name of the external user."""
        return self.properties.get("DisplayName", None)

    @property
    def invited_as(self) -> Optional[str]:
        """The email address or login name to which the invitation was sent."""
        return self.properties.get("InvitedAs", None)

    @property
    def invited_by(self) -> Optional[str]:
        """The login name of the user who invited this external user."""
        return self.properties.get("InvitedBy", None)

    @property
    def is_cross_tenant(self) -> Optional[bool]:
        """Whether the user belongs to another Microsoft 365 tenant."""
        return self.properties.get("IsCrossTenant", None)

    @property
    def login_name(self) -> Optional[str]:
        """The login name of the external user."""
        return self.properties.get("LoginName", None)

    @property
    def unique_id(self) -> Optional[str]:
        """A unique identifier for this external user."""
        return self.properties.get("UniqueId", None)

    @property
    def user_id(self) -> Optional[int]:
        """The SharePoint user ID of the external user."""
        return self.properties.get("UserId", None)

    @property
    def when_created(self) -> Optional[datetime]:
        """The date and time when the external user was created."""
        return self.properties.get("WhenCreated", None)

    @property
    def property_ref_name(self) -> str:
        return "AcceptedAs"

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantManagement.ExternalUser"
