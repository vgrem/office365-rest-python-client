from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.lifecycletaskcategory import LifecycleTaskCategory
from office365.directory.identitygovernance.parameter import Parameter
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class TaskDefinition(Entity):
    @odata(name="category")
    @property
    def category(self) -> LifecycleTaskCategory:
        """Gets the category property"""
        return self.properties.get("category", LifecycleTaskCategory.joiner)

    @odata(name="continueOnError")
    @property
    def continue_on_error(self) -> Optional[bool]:
        """Gets the continueOnError property"""
        return self.properties.get("continueOnError", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="parameters")
    @property
    def parameters(self) -> ClientValueCollection[Parameter]:
        """Gets the parameters property"""
        return self.properties.get("parameters", ClientValueCollection[Parameter](Parameter))

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.TaskDefinition"
