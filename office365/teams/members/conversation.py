from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection


class ConversationMember(Entity):
    """Represents a user in a team, a channel, or a chat. See also aadUserConversationMember."""

    def __str__(self) -> str:
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """The display name of the user."""
        return self.properties.get("displayName", None)

    @property
    def roles(self) -> StringCollection:
        """The roles for that user."""
        return self.properties.setdefault("roles", StringCollection())
