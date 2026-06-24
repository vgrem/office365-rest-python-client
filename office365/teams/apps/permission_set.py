from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.teams.apps.resource_specific_permission import TeamsAppResourceSpecificPermission


@dataclass
class TeamsAppPermissionSet(ClientValue):
    """Set of required/granted permissions that can be associated with a Teams app."""

    resourceSpecificPermissions: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(TeamsAppResourceSpecificPermission)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppPermissionSet"
