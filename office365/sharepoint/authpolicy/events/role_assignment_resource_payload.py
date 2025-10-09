from office365.runtime.client_value import ClientValue


class RoleAssignmentResourcePayload(ClientValue):

    def __init__(
        self,
        directory_scope_id: str = None,
        principal_id: str = None,
        role_definition_id: str = None,
    ):
        self.directoryScopeId = directory_scope_id
        self.principalId = principal_id
        self.roleDefinitionId = role_definition_id

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.Events.RoleAssignmentResourcePayload"
