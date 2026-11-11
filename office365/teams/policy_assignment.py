from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.teams.administration.policy_user_assignment import (
        TeamsPolicyUserAssignment,
    )
    from office365.teams.policy_identifier_detail import PolicyIdentifierDetail


class TeamsPolicyAssignment(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.TeamsPolicyAssignment"

    @odata(name="userAssignments", navigation=True)
    @property
    def user_assignments(self) -> EntityCollection[TeamsPolicyUserAssignment]:
        """Gets the userAssignments property"""
        from office365.teams.administration.policy_user_assignment import (
            TeamsPolicyUserAssignment,
        )

        return self.properties.get(
            "userAssignments",
            EntityCollection[TeamsPolicyUserAssignment](
                self.context, TeamsPolicyUserAssignment, ResourcePath("userAssignments", self.resource_path)
            ),
        )

    @require_permission(
        delegated=["TeamsPolicyUserAssign.ReadWrite.All"],
        application=["TeamsPolicyUserAssign.ReadWrite.All"],
    )
    def get_policy_id(self, type_: str, name: str) -> EntityCollection[PolicyIdentifierDetail]:
        """getPolicyId operation.

        Args:
            type_ (str):
                type parameter
            name (str):
                name parameter
        """
        from office365.teams.policy_identifier_detail import PolicyIdentifierDetail

        return_type = EntityCollection(self.context, PolicyIdentifierDetail)
        qry = FunctionQuery(self, "getPolicyId", {"type": type_, "name": name}, return_type)
        self.context.add_query(qry)
        return return_type
