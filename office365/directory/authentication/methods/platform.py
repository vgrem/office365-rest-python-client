from enum import Enum


class AuthenticationMethodPlatform(Enum):
    unknown = "0"
    windows = "1"
    macOS = "2"
    iOS = "3"
    android = "4"
    linux = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodPlatform"
