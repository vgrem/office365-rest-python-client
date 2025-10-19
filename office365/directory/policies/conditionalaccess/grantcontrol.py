from enum import Enum


class ConditionalAccessGrantControl(Enum):
    block = "0"
    mfa = "1"
    compliantDevice = "2"
    domainJoinedDevice = "3"
    approvedApplication = "4"
    compliantApplication = "5"
    passwordChange = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessGrantControl"
