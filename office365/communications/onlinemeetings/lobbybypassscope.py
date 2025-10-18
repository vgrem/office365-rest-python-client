from enum import Enum


class LobbyBypassScope(Enum):
    organizer = "0"
    organization = "1"
    organizationAndFederated = "2"
    everyone = "3"
    unknownFutureValue = "4"
    invited = "5"
    organizationExcludingGuests = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LobbyBypassScope"
