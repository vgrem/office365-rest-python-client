from enum import Enum


class WindowsHelloForBusinessPinUsage(Enum):
    allowed = "0"
    required = "1"
    disallowed = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsHelloForBusinessPinUsage"
