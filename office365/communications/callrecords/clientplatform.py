from enum import Enum


class ClientPlatform(Enum):
    unknown = "0"
    windows = "1"
    macOS = "2"
    iOS = "3"
    android = "4"
    web = "5"
    ipPhone = "6"
    roomSystem = "7"
    surfaceHub = "8"
    holoLens = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.callRecords.ClientPlatform"
