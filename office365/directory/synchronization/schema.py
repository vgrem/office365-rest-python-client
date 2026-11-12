from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.synchronization.attribute_mapping_function_schema import (
    AttributeMappingFunctionSchema,
)
from office365.directory.synchronization.directory_definition import DirectoryDefinition
from office365.directory.synchronization.rule import SynchronizationRule
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.synchronization.filter_operator_schema import FilterOperatorSchema
    from office365.security.attribute_definition import AttributeDefinition
    from office365.security.expression_input_object import ExpressionInputObject
    from office365.security.parse_expression_response import ParseExpressionResponse


class SynchronizationSchema(Entity):
    """
    Defines what objects will be synchronized and how they will be synchronized. The synchronization schema contains
    most of the setup information for a particular synchronization job. Typically, you will customize some of the
    attribute mappings, or add a scoping filter to synchronize only objects that satisfy a certain condition.

    The following sections describe the high-level components of the synchronization schema.
    """

    @verb(role="action", effect="read")
    @require_permission(delegated=["Synchronization.Read.All"], application=["Synchronization.Read.All"])
    def functions(self) -> EntityCollection[AttributeMappingFunctionSchema]:
        """List all the functions currently supported in the attributeMappingSource."""
        return_type = EntityCollection(self.context, AttributeMappingFunctionSchema)
        qry = FunctionQuery(self, "functions", None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="directories", navigation=True)
    @property
    def directories(self) -> EntityCollection[DirectoryDefinition]:
        """Contains the collection of directories and all of their objects."""
        return self.properties.get(
            "directories",
            EntityCollection(self.context, DirectoryDefinition, ResourcePath("directories", self.resource_path)),
        )

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationSchema"

    @odata(name="synchronizationRules")
    @property
    def synchronization_rules(self) -> ClientValueCollection[SynchronizationRule]:
        """Gets the synchronizationRules property"""
        return self.properties.get(
            "synchronizationRules", ClientValueCollection[SynchronizationRule](SynchronizationRule)
        )

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["Synchronization.ReadWrite.All"],
        application=["Application.ReadWrite.OwnedBy", "Synchronization.ReadWrite.All"],
    )
    def parse_expression(
        self, expression: str, test_input_object: ExpressionInputObject, target_attribute_definition: AttributeDefinition
    ) -> ClientResult[ParseExpressionResponse]:
        """parseExpression operation.

        Args:
            expression (str):
                expression parameter
            test_input_object (ExpressionInputObject):
                testInputObject parameter
            target_attribute_definition (AttributeDefinition):
                targetAttributeDefinition parameter
        """
        from office365.security.parse_expression_response import ParseExpressionResponse

        return_type = ClientResult(self.context, ParseExpressionResponse())
        qry = ServiceOperationQuery(
            self,
            "parseExpression",
            None,
            {
                "expression": expression,
                "testInputObject": test_input_object,
                "targetAttributeDefinition": target_attribute_definition,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="read")
    @require_permission(
        delegated=["Synchronization.ReadWrite.All"],
        application=["Application.ReadWrite.OwnedBy", "Synchronization.ReadWrite.All"],
    )
    def filter_operators(self) -> EntityCollection[FilterOperatorSchema]:
        """filterOperators operation."""
        from office365.directory.synchronization.filter_operator_schema import FilterOperatorSchema

        return_type = EntityCollection(self.context, FilterOperatorSchema)
        qry = FunctionQuery(self, "filterOperators", None, return_type)
        self.context.add_query(qry)
        return return_type
