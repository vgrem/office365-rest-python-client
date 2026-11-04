from __future__ import annotations

from office365.directory.subjectset import SubjectSet
from office365.runtime.types.value import value


@value
class SingleUser(SubjectSet):
    description: str | None = None
    userId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SingleUser"
