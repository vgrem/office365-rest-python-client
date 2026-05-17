from enum import Enum


class UserDefaultAuthenticationMethod(Enum):
    push = "0"
    oath = "1"
    voiceMobile = "2"
    voiceAlternateMobile = "3"
    voiceOffice = "4"
    sms = "5"
    none = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserDefaultAuthenticationMethod"
