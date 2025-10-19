from enum import Enum


class AttributeDefinitionMetadata(Enum):
    BaseAttributeName = "0"
    ComplexObjectDefinition = "1"
    IsContainer = "2"
    IsCustomerDefined = "3"
    IsDomainQualified = "4"
    LinkPropertyNames = "5"
    LinkTypeName = "6"
    MaximumLength = "7"
    ReferencedProperty = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttributeDefinitionMetadata"
