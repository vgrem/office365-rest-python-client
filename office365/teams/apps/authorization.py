from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.apps.permission_set import TeamsAppPermissionSet


@dataclass
class TeamsAppAuthorization(ClientValue):
    """The authorization details of a teamsApp.

    :param str client_app_id: 	The registration ID of the Microsoft Entra app ID associated with the teamsApp.
    :param TeamsAppPermissionSet required_permission_set: Set of permissions required by the teamsApp.
    """

    clientAppId: str | None = None
    requiredPermissionSet: TeamsAppPermissionSet = field(default_factory=TeamsAppPermissionSet)
