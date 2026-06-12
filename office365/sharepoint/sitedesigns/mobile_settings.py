from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.tab_item import TabItem


class MobileSettings(ClientValue):
    tabs: ClientValueCollection[TabItem] = field(default_factory=lambda: ClientValueCollection(TabItem))
