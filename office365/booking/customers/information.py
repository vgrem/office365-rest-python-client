from __future__ import annotations

from dataclasses import dataclass

from office365.booking.questionanswer import BookingQuestionAnswer
from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class BookingCustomerInformation(ClientValue):
    customerId: str | None = None
    customQuestionAnswers: ClientValueCollection[BookingQuestionAnswer] | None = None
    emailAddress: str | None = None
    location: Location | None = None
    name: str | None = None
    notes: str | None = None
    phone: str | None = None
    timeZone: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingCustomerInformation"
