from __future__ import annotations

from dataclasses import dataclass

from office365.directory.subjectset import SubjectSet


@dataclass
class AttributeRuleMembers(SubjectSet):
    description: str | None = None
    membershipRule: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttributeRuleMembers"
