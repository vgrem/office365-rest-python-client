from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class SchemaExtension(Entity):
    """Schema extensions allow you to define a schema to extend and add strongly-typed custom data to a resource type.
    The custom data appears as a complex type on the extended resource."""

    @odata(name="targetTypes")
    @property
    def target_types(self) -> StringCollection:
        """
        Set of Microsoft Graph types (that can support extensions) that the schema extension can be applied to.
        Select from administrativeUnit, contact, device, event, group, message, organization, post, todoTask,
        todoTaskList, or user.
        """
        return self.properties.get("targetTypes", StringCollection())

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="owner")
    @property
    def owner(self) -> Optional[str]:
        """Gets the owner property"""
        return self.properties.get("owner", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SchemaExtension"
