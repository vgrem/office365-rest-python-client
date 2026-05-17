from enum import Enum


class DirectoryDefinitionDiscoverabilities(Enum):
    None_ = "0"
    AttributeNames = "1"
    AttributeDataTypes = "2"
    AttributeReadOnly = "4"
    ReferenceAttributes = "8"
    UnknownFutureValue = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DirectoryDefinitionDiscoverabilities"
