from enum import Enum


class OnlineMeetingPresenters(Enum):
    everyone = "0"
    organization = "1"
    roleIsPresenter = "2"
    organizer = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnlineMeetingPresenters"
