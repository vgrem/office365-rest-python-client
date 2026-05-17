from enum import Enum


class ProvisioningStepType(Enum):
    import_ = "0"
    scoping = "1"
    matching = "2"
    processing = "3"
    referenceResolution = "4"
    export = "5"
    unknownFutureValue = "6"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStepType"
