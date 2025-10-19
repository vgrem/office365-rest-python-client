from enum import Enum


class UserAction(Enum):
    registerSecurityInformation = "0"
    registerOrJoinDevices = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserAction"
