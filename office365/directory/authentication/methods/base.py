from enum import Enum


class BaseAuthenticationMethod(Enum):
    password = "1"
    voice = "2"
    hardwareOath = "3"
    softwareOath = "4"
    sms = "5"
    fido2 = "6"
    windowsHelloForBusiness = "7"
    microsoftAuthenticator = "8"
    temporaryAccessPass = "9"
    email = "10"
    x509Certificate = "11"
    federation = "12"
    unknownFutureValue = "13"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BaseAuthenticationMethod"
