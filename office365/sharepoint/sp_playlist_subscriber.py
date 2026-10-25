from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPPlaylist_Subscriber(Entity):
    @odata(name="isUserSubscribed")
    @property
    def is_user_subscribed(self) -> Optional[bool]:
        """Gets the isUserSubscribed property"""
        return self.properties.get("isUserSubscribed", None)
