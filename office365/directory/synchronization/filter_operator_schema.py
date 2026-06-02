from __future__ import annotations

from office365.directory.synchronization.attributetype import AttributeType
from office365.directory.synchronization.scopeoperatormultivaluedcomparisontype import (
    ScopeOperatorMultiValuedComparisonType,
)
from office365.directory.synchronization.scopeoperatortype import ScopeOperatorType
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection


class FilterOperatorSchema(Entity):
    @property
    def arity(self) -> ScopeOperatorType:
        """Gets the arity property"""
        return self.properties.get("arity", ScopeOperatorType.Binary)

    @property
    def multivalued_comparison_type(self) -> ScopeOperatorMultiValuedComparisonType:
        """Gets the multivaluedComparisonType property"""
        return self.properties.get("multivaluedComparisonType", ScopeOperatorMultiValuedComparisonType.All)

    @property
    def supported_attribute_types(self) -> ClientValueCollection[AttributeType]:
        """Gets the supportedAttributeTypes property"""
        return self.properties.get("supportedAttributeTypes", ClientValueCollection[AttributeType](AttributeType))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FilterOperatorSchema"
