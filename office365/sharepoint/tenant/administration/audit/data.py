from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.eventdata import EventData
from office365.sharepoint.tenant.administration.modified_property import (
    ModifiedProperty,
)
from office365.sharepoint.tenant.administration.parameter import Parameter
from office365.sharepoint.tenant.administration.target_property import TargetProperty


@dataclass
class AuditData(ClientValue):
    ClientIP: str | None = None
    CorrelationId: str | None = None
    EventSource: str | None = None
    ItemType: str | None = None
    ListItemUniqueId: str | None = None
    ModifiedProperties: ClientValueCollection[ModifiedProperty] = field(
        default_factory=lambda: ClientValueCollection(ModifiedProperty)
    )
    Site: str | None = None
    TeamName: str | None = None
    UserId: str | None = None
    CreationTime: datetime | None = None
    EventData: str | None = None
    EventDataParsed: EventData = field(default_factory=lambda: EventData())
    Id: str | None = None
    Name: str | None = None
    NewValue: str | None = None
    ObjectId: str | None = None
    OldValue: str | None = None
    Parameters: ClientValueCollection[Parameter] = field(
        default_factory=lambda: ClientValueCollection(Parameter)
    )
    Target: ClientValueCollection[TargetProperty] = field(
        default_factory=lambda: ClientValueCollection(TargetProperty)
    )
    TargetUserOrGroupName: str | None = None
    TargetUserOrGroupType: str | None = None
    UserType: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuditData"
