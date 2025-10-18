from enum import Enum


class NativeAuthenticationApisEnabled(Enum):
    none = "0"
    all = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.NativeAuthenticationApisEnabled"
