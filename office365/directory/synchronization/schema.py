from __future__ import annotations

from typing import Optional

from office365.directory.synchronization.attribute_mapping_function_schema import (
    AttributeMappingFunctionSchema,
)
from office365.directory.synchronization.directory_definition import DirectoryDefinition
from office365.directory.synchronization.rule import SynchronizationRule
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata


class SynchronizationSchema(Entity):
    """
    Defines what objects will be synchronized and how they will be synchronized. The synchronization schema contains
    most of the setup information for a particular synchronization job. Typically, you will customize some of the
    attribute mappings, or add a scoping filter to synchronize only objects that satisfy a certain condition.

    The following sections describe the high-level components of the synchronization schema.
    """

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
