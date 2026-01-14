from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.eventdata import EventData
from office365.sharepoint.tenant.administration.modified_property import (
    ModifiedProperty,
)
from office365.sharepoint.tenant.administration.parameter import Parameter
from office365.sharepoint.tenant.administration.target_property import TargetProperty


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
        creation_time: datetime = None,
        event_data: str = None,
        event_data_parsed: EventData = EventData(),
        id_: str = None,
        name: str = None,
        new_value: str = None,
        object_id: str = None,
        old_value: str = None,
        parameters: ClientValueCollection[Parameter] = ClientValueCollection(Parameter),
        target: ClientValueCollection[TargetProperty] = ClientValueCollection(TargetProperty),
        target_user_or_group_name: str = None,
        target_user_or_group_type: str = None,
        user_type: int = None,
    ):
        self.ClientIP = client_ip
        self.CorrelationId = correlation_id
        self.EventSource = event_source
        self.ItemType = item_type
        self.ListItemUniqueId = list_item_unique_id
        self.ModifiedProperties = ClientValueCollection(ModifiedProperty, modified_properties)
        self.Site = site
        self.TeamName = team_name
        self.UserId = user_id
        self.CreationTime = creation_time
        self.EventData = event_data
        self.EventDataParsed = event_data_parsed
        self.Id = id_
        self.Name = name
        self.NewValue = new_value
        self.ObjectId = object_id
        self.OldValue = old_value
        self.Parameters = parameters
        self.Target = target
        self.TargetUserOrGroupName = target_user_or_group_name
        self.TargetUserOrGroupType = target_user_or_group_type
        self.UserType = user_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuditData"
