from typing import List

from office365.directory.groups.grouptype import GroupType
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.modified_property import ModifiedProperty


class TargetResource(ClientValue):
    """Represents target resource types associated with audit activity."""

    def __init__(
        self,
        display_name: str = None,
        modified_properties: List[ModifiedProperty] = None,
        user_principal_name: str = None,
        group_type: GroupType = GroupType.none,
        id_: str = None,
        type_: str = None,
    ):
        self.displayName = display_name
        self.ModifiedProperties = ClientValueCollection(ModifiedProperty, modified_properties)
        self.userPrincipalName = user_principal_name
        self.groupType = group_type
        self.id = id_
        self.type = type_

    @property
    def entity_type_name(self):
        return "microsoft.graph.TargetResource"
