from enum import Enum


class IncludedUserRoles(Enum):
    """"""

    all = "0"

    privilegedAdmin = "1"

    admin = "2"

    user = "3"

    unknownFutureValue = "4"


class AuthenticationMethodFeature(Enum):
    """"""

    ssprRegistered = "0"

    ssprEnabled = "1"

    ssprCapable = "2"

    passwordlessCapable = "3"

    mfaCapable = "4"

    unknownFutureValue = "5"
