from enum import Enum


class MessageActionFlag(Enum):
    any = "0"
    call = "1"
    doNotForward = "2"
    followUp = "3"
    fyi = "4"
    forward = "5"
    noResponseNecessary = "6"
    read = "7"
    reply = "8"
    replyToAll = "9"
    review = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MessageActionFlag"
