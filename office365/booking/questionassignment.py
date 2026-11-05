from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BookingQuestionAssignment(ClientValue):
    isRequired: bool | None = None
    questionId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingQuestionAssignment"
