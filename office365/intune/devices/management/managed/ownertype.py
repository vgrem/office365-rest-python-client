from enum import Enum


class ManagedDeviceOwnerType(Enum):
    unknown = "0"
    company = "1"
    personal = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedDeviceOwnerType"
