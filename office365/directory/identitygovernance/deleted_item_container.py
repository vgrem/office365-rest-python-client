from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.workflow.workflow import Workflow


class DeletedItemContainer(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeletedItemContainer"

    @odata(name="workflows", navigation=True)
    @property
    def workflows(self) -> EntityCollection[Workflow]:
        """Gets the workflows property"""
        from office365.directory.identitygovernance.workflow.workflow import Workflow

        return self.properties.get(
            "workflows",
            EntityCollection[Workflow](self.context, Workflow, ResourcePath("workflows", self.resource_path)),
        )
