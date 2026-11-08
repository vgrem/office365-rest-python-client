from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.error_code import ErrorCode
from office365.common.policy_set_status import PolicySetStatus
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.policy_set_assignment import PolicySetAssignment
    from office365.common.policy_set_item import PolicySetItem


@version("beta")
class PolicySet(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

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

    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[ErrorCode]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="guidedDeploymentTags")
    @property
    def guided_deployment_tags(self) -> StringCollection:
        """Gets the guidedDeploymentTags property"""
        return self.properties.get("guidedDeploymentTags", StringCollection())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="roleScopeTags")
    @property
    def role_scope_tags(self) -> StringCollection:
        """Gets the roleScopeTags property"""
        return self.properties.get("roleScopeTags", StringCollection())

    @odata(name="status")
    @property
    def status(self) -> Optional[PolicySetStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[PolicySetAssignment]:
        """Gets the assignments property"""
        from office365.common.policy_set_assignment import PolicySetAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[PolicySetAssignment](
                self.context, PolicySetAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="items", navigation=True)
    @property
    def items(self) -> EntityCollection[PolicySetItem]:
        """Gets the items property"""
        from office365.common.policy_set_item import PolicySetItem

        return self.properties.get(
            "items",
            EntityCollection[PolicySetItem](self.context, PolicySetItem, ResourcePath("items", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicySet"
