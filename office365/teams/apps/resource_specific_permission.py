from office365.runtime.client_value import ClientValue
from office365.teams.apps.resourcespecificpermissiontype import TeamsAppResourceSpecificPermissionType


class TeamsAppResourceSpecificPermission(ClientValue):
    permissionType: TeamsAppResourceSpecificPermissionType = TeamsAppResourceSpecificPermissionType.delegated
    permissionValue: str | None = None
    "Represents the resource-specific permission associated with a teamsApp."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppResourceSpecificPermission"
