from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.navigation.menu.node import MenuNode


class MenuState(ClientValue):
    """A menu tree which can be shown in the Quick Launch of a site."""

    AudienceIds: GuidCollection = field(default_factory=GuidCollection)
    FriendlyUrlPrefix: str | None = None
    Nodes: ClientValueCollection[MenuNode] = field(default_factory=lambda: ClientValueCollection(MenuNode))
    SimpleUrl: str | None = None
    SPSitePrefix: str | None = None
    IsAudienceTargetEnabledForGlobalNav: bool | None = None
    SPWebPrefix: str | None = None
    StartingNodeKey: str | None = None
    StartingNodeTitle: str | None = None
    Version: str | None = None
