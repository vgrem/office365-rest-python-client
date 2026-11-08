from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.ingestion_source import IngestionSource
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_category import GroupPolicyCategory
    from office365.common.group_policy_definition import GroupPolicyDefinition
    from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile


@version("beta")
class GroupPolicyCategory(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="ingestionSource")
    @property
    def ingestion_source(self) -> Optional[IngestionSource]:
        """Gets the ingestionSource property"""
        return self.properties.get("ingestionSource", None)

    @odata(name="isRoot")
    @property
    def is_root(self) -> Optional[bool]:
        """Gets the isRoot property"""
        return self.properties.get("isRoot", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="children", navigation=True)
    @property
    def children(self) -> EntityCollection[GroupPolicyCategory]:
        """Gets the children property"""
        from office365.common.group_policy_category import GroupPolicyCategory

        return self.properties.get(
            "children",
            EntityCollection[GroupPolicyCategory](
                self.context, GroupPolicyCategory, ResourcePath("children", self.resource_path)
            ),
        )

    @odata(name="definitionFile", navigation=True)
    @property
    def definition_file(self) -> GroupPolicyDefinitionFile:
        """Gets the definitionFile property"""
        from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile

        return self.properties.get(
            "definitionFile", GroupPolicyDefinitionFile(self.context, ResourcePath("definitionFile", self.resource_path))
        )

    @odata(name="definitions", navigation=True)
    @property
    def definitions(self) -> EntityCollection[GroupPolicyDefinition]:
        """Gets the definitions property"""
        from office365.common.group_policy_definition import GroupPolicyDefinition

        return self.properties.get(
            "definitions",
            EntityCollection[GroupPolicyDefinition](
                self.context, GroupPolicyDefinition, ResourcePath("definitions", self.resource_path)
            ),
        )

    @odata(name="parent", navigation=True)
    @property
    def parent(self) -> GroupPolicyCategory:
        """Gets the parent property"""
        from office365.common.group_policy_category import GroupPolicyCategory

        return self.properties.get(
            "parent", GroupPolicyCategory(self.context, ResourcePath("parent", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyCategory"
