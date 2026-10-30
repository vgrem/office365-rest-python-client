from __future__ import annotations

from office365.communications.virtualevents.registrationquestionanswerinputtype import (  # noqa: E501
    VirtualEventRegistrationQuestionAnswerInputType,
)
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


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
        return self.properties.get("answerInputType", VirtualEventRegistrationQuestionAnswerInputType.text)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistrationCustomQuestion"
