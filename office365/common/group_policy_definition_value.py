from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.group_policy_configuration_type import GroupPolicyConfigurationType
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_definition import GroupPolicyDefinition
    from office365.common.group_policy_presentation_value import GroupPolicyPresentationValue


@version("beta")
class GroupPolicyDefinitionValue(Entity):
    @odata(name="configurationType")
    @property
    def configuration_type(self) -> Optional[GroupPolicyConfigurationType]:
        """Gets the configurationType property"""
        return self.properties.get("configurationType", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="enabled")
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the enabled property"""
        return self.properties.get("enabled", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="definition", navigation=True)
    @property
    def definition(self) -> GroupPolicyDefinition:
        """Gets the definition property"""
        from office365.common.group_policy_definition import GroupPolicyDefinition

        return self.properties.get(
            "definition", GroupPolicyDefinition(self.context, ResourcePath("definition", self.resource_path))
        )

    @odata(name="presentationValues", navigation=True)
    @property
    def presentation_values(self) -> EntityCollection[GroupPolicyPresentationValue]:
        """Gets the presentationValues property"""
        from office365.common.group_policy_presentation_value import GroupPolicyPresentationValue

        return self.properties.get(
            "presentationValues",
            EntityCollection[GroupPolicyPresentationValue](
                self.context, GroupPolicyPresentationValue, ResourcePath("presentationValues", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyDefinitionValue"
