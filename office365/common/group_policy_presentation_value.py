from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_definition_value import GroupPolicyDefinitionValue
    from office365.common.group_policy_presentation import GroupPolicyPresentation


@version("beta")
class GroupPolicyPresentationValue(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="definitionValue", navigation=True)
    @property
    def definition_value(self) -> GroupPolicyDefinitionValue:
        """Gets the definitionValue property"""
        from office365.common.group_policy_definition_value import GroupPolicyDefinitionValue

        return self.properties.get(
            "definitionValue",
            GroupPolicyDefinitionValue(self.context, ResourcePath("definitionValue", self.resource_path)),
        )

    @odata(name="presentation", navigation=True)
    @property
    def presentation(self) -> GroupPolicyPresentation:
        """Gets the presentation property"""
        from office365.common.group_policy_presentation import GroupPolicyPresentation

        return self.properties.get(
            "presentation", GroupPolicyPresentation(self.context, ResourcePath("presentation", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyPresentationValue"
