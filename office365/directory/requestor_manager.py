from __future__ import annotations

from office365.directory.subjectset import SubjectSet


class RequestorManager(SubjectSet):
    managerLevel: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RequestorManager"
