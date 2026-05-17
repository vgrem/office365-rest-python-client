from enum import Enum


class ObjectDefinitionMetadata(Enum):
    PropertyNameAccountEnabled = "0"
    PropertyNameSoftDeleted = "1"
    IsSoftDeletionSupported = "2"
    IsSynchronizeAllSupported = "3"
    ConnectorDataStorageRequired = "4"
    Extensions = "5"
    BaseObjectName = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ObjectDefinitionMetadata"
