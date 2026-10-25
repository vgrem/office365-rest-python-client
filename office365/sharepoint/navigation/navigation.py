from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.navigation.nodes.collection import NavigationNodeCollection

if TYPE_CHECKING:
    from office365.runtime.progress import Progress
    from office365.sharepoint.navigation.nodes.node import NavigationNode


class Navigation(Entity):
    """Represents navigation operations at the site collection level."""

    def get_tree(
        self,
        recursive: bool = True,
        progress: Optional[Callable[[Progress[NavigationNode]], None]] = None,
    ) -> Self:
        """Queue a read of this navigation and of every node's descendants in both bars.

        Both bars are navigations, so they have to be expanded for the response to carry
        them as typed collections (a plain read returns only their URIs, and each property
        builds a fresh collection per access); every expanded bar is then walked with
        :meth:`NavigationNodeCollection.get_all_nodes`. Execute the queued queries to get
        the whole tree::

            navigation = web.navigation.get_tree().execute_query()
            navigation.quick_launch[0].children[0].title

        Args:
            recursive (bool): Whether to walk child nodes recursively (default True).
            progress: Optional hook invoked per visited node, shared by both bars.

        Returns:
            The current instance for method chaining.
        """

        def _walk(_) -> None:
            self.quick_launch.get_all_nodes(recursive, progress)
            self.top_navigation_bar.get_all_nodes(recursive, progress)

        return self.expand(["QuickLaunch", "TopNavigationBar"]).get().after_execute(_walk)

    @odata(name="UseShared")
    @property
    def use_shared(self) -> bool | None:
        """Gets a value that specifies whether the site inherits navigation."""
        return self.properties.get("UseShared", None)

    @use_shared.setter
    def use_shared(self, value: bool):
        """Sets a value that specifies whether the site inherits navigation."""
        self.set_property("UseShared", value)

    @odata(name="QuickLaunch", navigation=True)
    @property
    def quick_launch(self) -> NavigationNodeCollection:
        """Gets a value that collects navigation nodes corresponding to links in the Quick Launch area of the site."""
        return self.properties.get(
            "QuickLaunch",
            NavigationNodeCollection(self.context, ResourcePath("QuickLaunch", self.resource_path)),
        )

    @odata(name="TopNavigationBar", navigation=True)
    @property
    def top_navigation_bar(self) -> NavigationNodeCollection:
        """Gets a value that collects navigation nodes corresponding to links in the top navigation bar of the site."""
        return self.properties.get(
            "TopNavigationBar",
            NavigationNodeCollection(self.context, ResourcePath("TopNavigationBar", self.resource_path)),
        )
