from typing import Optional

from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.entity import Entity
from office365.sharepoint.microfeed.entity import MicroBlogEntity


class MicrofeedManager(Entity):
    def __init__(self, context):
        super().__init__(context, StaticPath("SP.Microfeed.MicrofeedManager"))

    @property
    def current_user(self) -> MicroBlogEntity:
        """Gets the CurrentUser property"""
        return self.properties.get("CurrentUser", MicroBlogEntity())

    @property
    def is_feed_activity_public(self) -> Optional[bool]:
        """Gets the IsFeedActivityPublic property"""
        return self.properties.get("IsFeedActivityPublic", None)

    @property
    def static_thread_link(self) -> Optional[str]:
        """Gets the StaticThreadLink property"""
        return self.properties.get("StaticThreadLink", None)

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedManager"
