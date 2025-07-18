from typing import Optional

from office365.entity import Entity


class Community(Entity):
    """Represents a community in Viva Engage that is a central place for conversations, files, events, and
     updates for people sharing a common interest or goal.

    Every community is associated with a Microsoft 365 group, but the group doesn't have the same ID as the community.
    For more information about managing communities in Viva Engage, see Use the Microsoft Graph API to work
    with Viva Engage.

    This resource is an open type that allows other properties to be passed in.
    """

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """The name of the community. The maximum length is 255 characters."""
        return self.properties.get("displayName", None)

    @property
    def description(self) -> Optional[str]:
        """The description of the community. The maximum length is 1,024 characters."""
        return self.properties.get("description", None)
