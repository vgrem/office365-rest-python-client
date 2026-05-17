from typing import Optional

from office365.sharepoint.entity import Entity


class SPPlaylistSubscriber(Entity):
    @property
    def is_user_subscribed(self) -> Optional[bool]:
        """Gets the isUserSubscribed property"""
        return self.properties.get("isUserSubscribed", None)
