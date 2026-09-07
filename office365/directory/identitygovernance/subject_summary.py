from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SubjectSummary(ClientValue):
    failedSubjects: int | None = None
    failedTasks: int | None = None
    successfulSubjects: int | None = None
    totalSubjects: int | None = None
    totalTasks: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.SubjectSummary"
