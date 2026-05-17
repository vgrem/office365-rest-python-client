from enum import Enum


class VirtualEventRegistrationPredefinedQuestionLabel(Enum):
    street = "0"
    city = "1"
    state = "2"
    postalCode = "3"
    countryOrRegion = "4"
    industry = "5"
    jobTitle = "6"
    organization = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VirtualEventRegistrationPredefinedQuestionLabel"
