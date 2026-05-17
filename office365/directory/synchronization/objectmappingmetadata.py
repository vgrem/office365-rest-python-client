from enum import Enum


class ObjectMappingMetadata(Enum):
    EscrowBehavior = "0"
    DisableMonitoringForChanges = "1"
    OriginalJoiningProperty = "2"
    Disposition = "3"
    IsCustomerDefined = "4"
    ExcludeFromReporting = "5"
    Unsynchronized = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ObjectMappingMetadata"
