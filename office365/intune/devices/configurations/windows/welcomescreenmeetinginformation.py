from enum import Enum


class WelcomeScreenMeetingInformation(Enum):
    userDefined = "0"
    showOrganizerAndTimeOnly = "1"
    showOrganizerAndTimeAndSubject = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WelcomeScreenMeetingInformation"
