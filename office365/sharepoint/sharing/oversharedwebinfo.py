from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


class OversharedWebInfo(ClientValue):

    def __init__(
        self,
        has_unique_role_assignments_for_list: bool = None,
        principals: ClientValueCollection[Principal] = ClientValueCollection(Principal),
    ):
        self.hasUniqueRoleAssignmentsForList = has_unique_role_assignments_for_list
        self.principals = principals

    @property
    def entity_type_name(self):
        return "SP.Sharing.OversharedWebInfo"
