from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.common.group_policy_definition_class_type import GroupPolicyDefinitionClassType
from office365.common.group_policy_type import GroupPolicyType
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_category import GroupPolicyCategory
    from office365.common.group_policy_definition import GroupPolicyDefinition
    from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile
    from office365.common.group_policy_presentation import GroupPolicyPresentation


@version("beta")
class GroupPolicyDefinition(Entity):
    @odata(name="categoryPath")
    @property
    def category_path(self) -> Optional[str]:
        """Gets the categoryPath property"""
        return self.properties.get("categoryPath", None)

    @odata(name="classType")
    @property
    def class_type(self) -> Optional[GroupPolicyDefinitionClassType]:
        """Gets the classType property"""
        return self.properties.get("classType", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="explainText")
    @property
    def explain_text(self) -> Optional[str]:
        """Gets the explainText property"""
        return self.properties.get("explainText", None)

    @odata(name="groupPolicyCategoryId")
    @property
    def group_policy_category_id(self) -> Optional[UUID]:
        """Gets the groupPolicyCategoryId property"""
        return self.properties.get("groupPolicyCategoryId", None)

    @odata(name="hasRelatedDefinitions")
    @property
    def has_related_definitions(self) -> Optional[bool]:
        """Gets the hasRelatedDefinitions property"""
        return self.properties.get("hasRelatedDefinitions", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="minDeviceCspVersion")
    @property
    def min_device_csp_version(self) -> Optional[str]:
        """Gets the minDeviceCspVersion property"""
        return self.properties.get("minDeviceCspVersion", None)

    @odata(name="minUserCspVersion")
    @property
    def min_user_csp_version(self) -> Optional[str]:
        """Gets the minUserCspVersion property"""
        return self.properties.get("minUserCspVersion", None)

    @odata(name="policyType")
    @property
    def policy_type(self) -> Optional[GroupPolicyType]:
        """Gets the policyType property"""
        return self.properties.get("policyType", None)

    @odata(name="supportedOn")
    @property
    def supported_on(self) -> Optional[str]:
        """Gets the supportedOn property"""
        return self.properties.get("supportedOn", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="category", navigation=True)
    @property
    def category(self) -> GroupPolicyCategory:
        """Gets the category property"""
        from office365.common.group_policy_category import GroupPolicyCategory

        return self.properties.get(
            "category", GroupPolicyCategory(self.context, ResourcePath("category", self.resource_path))
        )

    @odata(name="definitionFile", navigation=True)
    @property
    def definition_file(self) -> GroupPolicyDefinitionFile:
        """Gets the definitionFile property"""
        from office365.common.group_policy_definition_file import GroupPolicyDefinitionFile

        return self.properties.get(
            "definitionFile", GroupPolicyDefinitionFile(self.context, ResourcePath("definitionFile", self.resource_path))
        )

    @odata(name="nextVersionDefinition", navigation=True)
    @property
    def next_version_definition(self) -> GroupPolicyDefinition:
        """Gets the nextVersionDefinition property"""
        from office365.common.group_policy_definition import GroupPolicyDefinition

        return self.properties.get(
            "nextVersionDefinition",
            GroupPolicyDefinition(self.context, ResourcePath("nextVersionDefinition", self.resource_path)),
        )

    @odata(name="presentations", navigation=True)
    @property
    def presentations(self) -> EntityCollection[GroupPolicyPresentation]:
        """Gets the presentations property"""
        from office365.common.group_policy_presentation import GroupPolicyPresentation

        return self.properties.get(
            "presentations",
            EntityCollection[GroupPolicyPresentation](
                self.context, GroupPolicyPresentation, ResourcePath("presentations", self.resource_path)
            ),
        )

    @odata(name="previousVersionDefinition", navigation=True)
    @property
    def previous_version_definition(self) -> GroupPolicyDefinition:
        """Gets the previousVersionDefinition property"""
        from office365.common.group_policy_definition import GroupPolicyDefinition

        return self.properties.get(
            "previousVersionDefinition",
            GroupPolicyDefinition(self.context, ResourcePath("previousVersionDefinition", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyDefinition"
