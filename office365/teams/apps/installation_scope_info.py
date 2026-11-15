from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.teams.apps.installation_scopes import TeamsAppInstallationScopes


class TeamsAppInstallationScopeInfo(ClientValue):
    scope: TeamsAppInstallationScopes = TeamsAppInstallationScopes.team

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppInstallationScopeInfo"
