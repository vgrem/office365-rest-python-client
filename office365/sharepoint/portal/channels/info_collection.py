from __future__ import annotations

from datetime import datetime

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.channels.info import ChannelInfo


@dataclass
class ChannelInfoCollection(ClientValue):
    value: ClientValueCollection[ChannelInfo] = field(default_factory=lambda: ClientValueCollection(ChannelInfo))
    CacheUpdatedTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ChannelInfoCollection"
