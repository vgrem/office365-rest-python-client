from __future__ import annotations

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.navigation.nodes.collection import NavigationNodeCollection


class Navigation(Entity):
    """Represents navigation operations at the site collection level."""

    @property
    def use_shared(self) -> bool | None:
        """Gets a value that specifies whether the site inherits navigation."""
        return self.properties.get("UseShared", None)

    @use_shared.setter
    def use_shared(self, value: bool):
        """Sets a value that specifies whether the site inherits navigation."""
        self.set_property("UseShared", value)

    @odata(name="QuickLaunch")
    @property
    def quick_launch(self) -> NavigationNodeCollection:
        """Gets a value that collects navigation nodes corresponding to links in the Quick Launch area of the site."""
        return self.properties.get(
            "QuickLaunch",
            NavigationNodeCollection(self.context, ResourcePath("QuickLaunch", self.resource_path)),
        )

    @odata(name="TopNavigationBar")
    @property
    def top_navigation_bar(self) -> NavigationNodeCollection:
        """Gets a value that collects navigation nodes corresponding to links in the top navigation bar of the site."""
        return self.properties.get(
            "TopNavigationBar",
            NavigationNodeCollection(self.context, ResourcePath("TopNavigationBar", self.resource_path)),
        )
