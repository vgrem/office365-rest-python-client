from datetime import datetime
from typing import Optional

from office365.entity import Entity


class Post(Entity):
    """Represents an individual Post item within a conversationThread entity."""

    @property
    def conversation_id(self) -> Optional[str]:
        """The ID of the conversation the post belongs to."""
        return self.properties.get("conversationId", None)

    @property
    def received_datetime(self) -> datetime:
        """The date and time the post was received."""
        return self.properties.get("receivedDateTime", datetime.min)
