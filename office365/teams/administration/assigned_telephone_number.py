from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.administration.assignment_category import AssignmentCategory


@value
class AssignedTelephoneNumber(ClientValue):
    assignmentCategory: AssignmentCategory = AssignmentCategory()
    telephoneNumber: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AssignedTelephoneNumber"
