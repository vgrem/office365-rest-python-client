from typing import Optional

from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.entity import Entity
from office365.sharepoint.microfeed.entity import MicroBlogEntity


class MicrofeedManager(Entity):
    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("SP.Microfeed.MicrofeedManager")
        return self._resource_path

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
