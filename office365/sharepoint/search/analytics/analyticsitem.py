from office365.runtime.client_value import ClientValue


class AnalyticsItem(ClientValue):

    def __init__(self, id_: str = None, properties: dict = None):
        self.Id = id_
        self.Properties = properties

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsItem"
