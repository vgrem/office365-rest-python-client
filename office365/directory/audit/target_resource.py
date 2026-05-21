from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.groups.grouptype import GroupType
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.modified_property import ModifiedProperty


@dataclass
class TargetResource(ClientValue):
    """Represents target resource types associated with audit activity."""

    displayName: str | None = None
    ModifiedProperties: ClientValueCollection[ModifiedProperty] = field(default_factory=lambda: ClientValueCollection(ModifiedProperty))
    userPrincipalName: str | None = None
    groupType: GroupType = GroupType.none
    id: str | None = None
    type: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.TargetResource"
