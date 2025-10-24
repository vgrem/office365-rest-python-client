from enum import Enum


class TeamworkUserIdentityType(Enum):
    aadUser = "0"
    onPremiseAadUser = "1"
    anonymousGuest = "2"
    federatedUser = "3"
    personalMicrosoftAccountUser = "4"
    skypeUser = "5"
    phoneUser = "6"
    unknownFutureValue = "7"
    emailUser = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkUserIdentityType"
