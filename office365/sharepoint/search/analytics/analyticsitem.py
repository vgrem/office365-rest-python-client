from typing import Optional

from office365.runtime.client_value import ClientValue


class AnalyticsItem(ClientValue):
    def __init__(self, id_: Optional[str] = None, properties: Optional[dict] = None):
        self.Id = id_
        self.Properties = properties

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsItem"
