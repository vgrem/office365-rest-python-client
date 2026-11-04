from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.translation.resource_entry import SPResourceEntry


@value
class MenuNode(ClientValue):
    """
    Represents a navigation node in the navigation hierarchy. A navigation hierarchy is a tree structure of
    navigation nodes.
    """

    AudienceIds: list[str] | None = None
    CurrentLCID: int | None = None
    IsDeleted: bool | None = None
    IsHidden: bool | None = None
    Nodes: ClientValueCollection[MenuNode] = field(default_factory=lambda: ClientValueCollection(MenuNode))
    SimpleUrl: str | None = None
    Title: str | None = None
    Translations: ClientValueCollection[SPResourceEntry] = field(
        default_factory=lambda: ClientValueCollection(SPResourceEntry)
    )
    CustomProperties: dict | None = None
    FriendlyUrlSegment: str | None = None
    IsTitleForExistingLanguage: bool | None = None
    Key: str | None = None
    NodeType: int | None = None
    OpenInNewWindow: bool | None = None
