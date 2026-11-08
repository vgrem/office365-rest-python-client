from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_definition import GroupPolicyDefinition


@version("beta")
class GroupPolicyPresentation(Entity):
    @odata(name="label")
    @property
    def label(self) -> Optional[str]:
        """Gets the label property"""
        return self.properties.get("label", None)

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyPresentation"
