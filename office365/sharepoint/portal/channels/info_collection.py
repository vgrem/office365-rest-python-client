from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.portal.channels.info import ChannelInfo


@value
class ChannelInfoCollection(ClientValue):
    value: ClientValueCollection[ChannelInfo] = field(default_factory=lambda: ClientValueCollection(ChannelInfo))
    CacheUpdatedTime: datetime | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ChannelInfoCollection"
