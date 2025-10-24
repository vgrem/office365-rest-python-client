from enum import Enum


class AllowedLobbyAdmitterRoles(Enum):
    organizerAndCoOrganizersAndPresenters = "0"
    organizerAndCoOrganizers = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AllowedLobbyAdmitterRoles"
