from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.channels.info import ChannelInfo


class ChannelInfoCollection(ClientValue):
    def __init__(self, value=None, cache_updated_time: datetime = None):
        self.value = ClientValueCollection(ChannelInfo, value)
        self.CacheUpdatedTime = cache_updated_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ChannelInfoCollection"
