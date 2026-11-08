from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.group_policy_type import GroupPolicyType
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_definition import GroupPolicyDefinition


@version("beta")
class GroupPolicyDefinitionFile(Entity):
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

    @odata(name="fileName")
    @property
    def file_name(self) -> Optional[str]:
        """Gets the fileName property"""
        return self.properties.get("fileName", None)

    @odata(name="languageCodes")
    @property
    def language_codes(self) -> StringCollection:
        """Gets the languageCodes property"""
        return self.properties.get("languageCodes", StringCollection())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="policyType")
    @property
    def policy_type(self) -> Optional[GroupPolicyType]:
        """Gets the policyType property"""
        return self.properties.get("policyType", None)

    @odata(name="revision")
    @property
    def revision(self) -> Optional[str]:
        """Gets the revision property"""
        return self.properties.get("revision", None)

    @odata(name="targetNamespace")
    @property
    def target_namespace(self) -> Optional[str]:
        """Gets the targetNamespace property"""
        return self.properties.get("targetNamespace", None)

    @odata(name="targetPrefix")
    @property
    def target_prefix(self) -> Optional[str]:
        """Gets the targetPrefix property"""
        return self.properties.get("targetPrefix", None)

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyDefinitionFile"
