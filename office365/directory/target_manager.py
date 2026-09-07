from __future__ import annotations

from dataclasses import dataclass

from office365.directory.subjectset import SubjectSet


@dataclass
class TargetManager(SubjectSet):
    managerLevel: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TargetManager"
