from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.translation.user_resource import UserResource

if TYPE_CHECKING:
    from office365.sharepoint.navigation.nodes.collection import (
        NavigationNodeCollection,
    )


class NavigationNode(Entity):
    """
    Represents the URL to a specific navigation node and provides access to properties and methods for
    manipulating the ordering of the navigation node in a navigation node collection.
    """

    def __str__(self):
        return self.title or self.entity_type_name

    def __repr__(self):
        return self.url or self.entity_type_name

    @odata(name="Id", readonly=True)
    @property
    def id(self) -> int | None:
        """Gets the unique identifier of the navigation node."""
        return self.properties.get("Id", None)

    @odata(name="Children", navigation=True)
    @property
    def children(self) -> NavigationNodeCollection:
        """Gets the collection of child nodes of the navigation node."""
        from office365.sharepoint.navigation.nodes.collection import (
            NavigationNodeCollection,
        )

        return self.properties.get(
            "Children",
            NavigationNodeCollection(self.context, ResourcePath("Children", self.resource_path)),
        )

    @odata(name="Title")
    @property
    def title(self) -> str | None:
        """Gets a value that specifies the anchor text for the navigation node link."""
        return self.properties.get("Title", None)

    @title.setter
    def title(self, value: str) -> None:
        """Sets a value that specifies the anchor text for the navigation node link."""
        self.set_property("Title", value)

    @odata(name="Url")
    @property
    def url(self) -> str | None:
        """Gets a value that specifies the URL stored with the navigation node."""
        return self.properties.get("Url", None)

    @url.setter
    def url(self, value: str) -> None:
        """Sets a value that specifies the URL stored with the navigation node."""
        self.set_property("Url", value)

    @odata(name="IsVisible", readonly=True)
    @property
    def is_visible(self) -> bool | None:
        """Gets a value that specifies whether the navigation node is shown in its navigation area."""
        return self.properties.get("IsVisible", None)

    @odata(name="IsExternal", readonly=True)
    @property
    def is_external(self) -> bool | None:
        """Gets a value that specifies whether the navigation node links outside the site."""
        return self.properties.get("IsExternal", None)

    @odata(name="TitleResource", navigation=True)
    @property
    def title_resource(self) -> UserResource:
        """Represents the title of this node."""
        return self.properties.get(
            "TitleResource",
            UserResource(self.context, ResourcePath("TitleResource", self.resource_path)),
        )

    @odata(name="AudienceIds")
    @property
    def audience_ids(self) -> GuidCollection:
        """Gets the AudienceIds property"""
        return self.properties.get("AudienceIds", GuidCollection())

    @odata(name="CurrentLCID", readonly=True)
    @property
    def current_lcid(self) -> Optional[int]:
        """Gets the CurrentLCID property"""
        return self.properties.get("CurrentLCID", None)

    @odata(name="IsDocLib", readonly=True)
    @property
    def is_doc_lib(self) -> Optional[bool]:
        """Gets the IsDocLib property"""
        return self.properties.get("IsDocLib", None)

    @odata(name="ListTemplateType", readonly=True)
    @property
    def list_template_type(self) -> Optional[int]:
        """Gets the ListTemplateType property"""
        return self.properties.get("ListTemplateType", None)
