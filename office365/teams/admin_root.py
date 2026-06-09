from __future__ import annotations

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.policy_assignment import TeamsPolicyAssignment


class TeamsAdminRoot(Entity):
    @property
    def policy(self) -> TeamsPolicyAssignment:
        """Gets the policy property"""
        return self.properties.get(
            "policy", TeamsPolicyAssignment(self.context, ResourcePath("policy", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TeamsAdminRoot"
