from enum import Enum


class DeviceLogCollectionTemplateType(Enum):
    predefined = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceLogCollectionTemplateType"
