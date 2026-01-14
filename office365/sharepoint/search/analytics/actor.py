from office365.runtime.client_value import ClientValue


class AnalyticsActor(ClientValue):
    def __init__(self, id_: str = None, properties: dict = None, tenant_id: str = None):
        self.Id = id_
        self.Properties = properties
        self.TenantId = tenant_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsActor"
