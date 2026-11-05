from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.teams.administration.assignment_category import AssignmentCategory


class AssignedTelephoneNumber(ClientValue):
    assignmentCategory: AssignmentCategory = field(default_factory=AssignmentCategory)
    telephoneNumber: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.AssignedTelephoneNumber"
