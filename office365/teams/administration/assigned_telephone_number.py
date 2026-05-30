from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.teams.administration.assignment_category import AssignmentCategory


@dataclass
class AssignedTelephoneNumber(ClientValue):
    assignmentCategory: AssignmentCategory = AssignmentCategory()
    telephoneNumber: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AssignedTelephoneNumber"
