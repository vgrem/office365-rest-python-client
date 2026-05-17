from enum import Enum


class UserFlowType(Enum):
    signUp = "1"
    signIn = "2"
    signUpOrSignIn = "3"
    passwordReset = "4"
    profileUpdate = "5"
    resourceOwner = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserFlowType"
