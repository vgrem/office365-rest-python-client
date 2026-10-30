from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.virtualevents.registrationquestionanswerinputtype import (
        VirtualEventRegistrationQuestionAnswerInputType,
    )


class VirtualEventRegistrationCustomQuestion(Entity):
    @odata(name="answerChoices")
    @property
    def answer_choices(self) -> StringCollection:
        """Gets the answerChoices property"""
        return self.properties.get("answerChoices", StringCollection())

    @odata(name="answerInputType")
    @property
    def answer_input_type(self) -> VirtualEventRegistrationQuestionAnswerInputType:
        """Gets the answerInputType property"""
        from office365.communications.virtualevents.registrationquestionanswerinputtype import (
            VirtualEventRegistrationQuestionAnswerInputType,
        )

        return self.properties.get("answerInputType", VirtualEventRegistrationQuestionAnswerInputType.text)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistrationCustomQuestion"
