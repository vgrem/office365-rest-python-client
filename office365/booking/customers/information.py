from office365.booking.questionanswer import BookingQuestionAnswer
from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingCustomerInformation(ClientValue):
    def __init__(
        self,
        customer_id: str = None,
        custom_question_answers: ClientValueCollection[BookingQuestionAnswer] = ClientValueCollection(
            BookingQuestionAnswer
        ),
        email_address: str = None,
        location: Location = Location(),
        name: str = None,
        notes: str = None,
        phone: str = None,
        time_zone: str = None,
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
