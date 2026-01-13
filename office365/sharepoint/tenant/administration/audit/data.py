from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.modified_property import (
    ModifiedProperty,
)


class AuditData(ClientValue):
    def __init__(
        self,
        client_ip=None,
        correlation_id=None,
        event_source=None,
        item_type=None,
        list_item_unique_id=None,
        modified_properties=None,
        site=None,
        team_name=None,
        user_id=None,
    ):
        self.ClientIP = client_ip
        self.CorrelationId = correlation_id
        self.EventSource = event_source
        self.ItemType = item_type
        self.ListItemUniqueId = list_item_unique_id
        self.ModifiedProperties = ClientValueCollection(
            ModifiedProperty, modified_properties
        )
        self.Site = site
        self.TeamName = team_name
        self.UserId = user_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuditData"
