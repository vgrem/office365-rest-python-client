from typing import Optional

from office365.runtime.client_value import ClientValue


class AnalyticsActor(ClientValue):
    def __init__(self, id_: Optional[str] = None, properties: Optional[dict] = None, tenant_id: Optional[str] = None):
        self.Id = id_
        self.Properties = properties
        self.TenantId = tenant_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Analytics.AnalyticsActor"
