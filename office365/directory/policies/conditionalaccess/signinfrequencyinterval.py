from enum import Enum


class SignInFrequencyInterval(Enum):
    timeBased = "0"
    everyTime = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SignInFrequencyInterval"
