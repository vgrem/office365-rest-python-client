from __future__ import annotations

from typing import List, Optional


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

    AudienceIds: Optional[List[str]] = None
    CurrentLCID: Optional[int] = None
    IsDeleted: Optional[bool] = None
    IsHidden: Optional[bool] = None
    Key = None
    Nodes: ClientValueCollection[MenuNode] | None = None
    NodeType = None
    OpenInNewWindow = None
    SimpleUrl: Optional[str] = None
    Title: Optional[str] = None
    Translations: ClientValueCollection[SPResourceEntry] | None = None
    CustomProperties: Optional[dict] = None
    FriendlyUrlSegment: Optional[str] = None
    IsTitleForExistingLanguage: Optional[bool] = None