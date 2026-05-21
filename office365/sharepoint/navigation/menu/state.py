from __future__ import annotations

from typing import List, Optional


from dataclasses import dataclass, field
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.navigation.menu.node import MenuNode


@dataclass
class MenuState(ClientValue):

    """A menu tree which can be shown in the Quick Launch of a site."""

    AudienceIds: GuidCollection = field(default_factory=GuidCollection)
    FriendlyUrlPrefix: Optional[str] = None
    Nodes: ClientValueCollection[MenuNode] | None = None
    SimpleUrl: Optional[str] = None
    SPSitePrefix: Optional[str] = None
    IsAudienceTargetEnabledForGlobalNav: Optional[bool] = None
    SPWebPrefix: Optional[str] = None
    StartingNodeKey: Optional[str] = None
    StartingNodeTitle: Optional[str] = None
    Version: Optional[str] = None