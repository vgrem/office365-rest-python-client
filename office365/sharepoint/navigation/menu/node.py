from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.translation.resource_entry import SPResourceEntry


@dataclass
class MenuNode(ClientValue):
    """
    Represents a navigation node in the navigation hierarchy. A navigation hierarchy is a tree structure of
    navigation nodes.
    """

    AudienceIds: list[str] | None = None
    CurrentLCID: int | None = None
    IsDeleted: bool | None = None
    IsHidden: bool | None = None
    Key = None
    Nodes: ClientValueCollection[MenuNode] | None = None
    NodeType = None
    OpenInNewWindow = None
    SimpleUrl: str | None = None
    Title: str | None = None
    Translations: ClientValueCollection[SPResourceEntry] | None = None
    CustomProperties: dict | None = None
    FriendlyUrlSegment: str | None = None
    IsTitleForExistingLanguage: bool | None = None
