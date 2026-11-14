from __future__ import annotations

from office365.communications.virtualevents.registration_question_base import VirtualEventRegistrationQuestionBase
from office365.communications.virtualevents.registrationpredefinedquestionlabel import (  # noqa: E501
    VirtualEventRegistrationPredefinedQuestionLabel,
)
from office365.runtime.types.odata_property import odata


class VirtualEventRegistrationPredefinedQuestion(VirtualEventRegistrationQuestionBase):
    @odata(name="label")
    @property
    def label(self) -> VirtualEventRegistrationPredefinedQuestionLabel:
        """Gets the label property"""
        return self.properties.get("label", VirtualEventRegistrationPredefinedQuestionLabel.street)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistrationPredefinedQuestion"
