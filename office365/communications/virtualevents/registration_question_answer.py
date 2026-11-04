from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class VirtualEventRegistrationQuestionAnswer(ClientValue):
    booleanValue: bool | None = None
    displayName: str | None = None
    multiChoiceValues: StringCollection = field(default_factory=StringCollection)
    questionId: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistrationQuestionAnswer"
