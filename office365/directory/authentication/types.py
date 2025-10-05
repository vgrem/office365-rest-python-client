from enum import Enum


class AuthenticationMethodModes(Enum):
    """"""

    password = "1"
    voice = "2"
    hardwareOath = "4"
    softwareOath = "8"
    sms = "16"
    fido2 = "32"
    windowsHelloForBusiness = "64"
    microsoftAuthenticatorPush = "128"
    deviceBasedPush = "256"
    temporaryAccessPassOneTime = "512"
    temporaryAccessPassMultiUse = "1024"
    email = "2048"
    x509CertificateSingleFactor = "4096"
    x509CertificateMultiFactor = "8192"
    federatedSingleFactor = "16384"
    federatedMultiFactor = "32768"
    unknownFutureValue = "65536"
