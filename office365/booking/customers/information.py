from typing import Optional

from office365.booking.questionanswer import BookingQuestionAnswer
from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingCustomerInformation(ClientValue):
    def __init__(
        self,
        customer_id: Optional[str] = None,
        custom_question_answers: Optional[ClientValueCollection[BookingQuestionAnswer]] = None,
        email_address: Optional[str] = None,
        location: Optional[Location] = None,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        phone: Optional[str] = None,
        time_zone: Optional[str] = None,
    ):
        self.customerId = customer_id
        self.customQuestionAnswers = custom_question_answers
        self.emailAddress = email_address
        self.location = location
        self.name = name
        self.notes = notes
        self.phone = phone
        self.timeZone = time_zone

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingCustomerInformation"
