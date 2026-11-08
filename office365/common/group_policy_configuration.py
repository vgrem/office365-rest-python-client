from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.common.group_policy_configuration_ingestion_type import GroupPolicyConfigurationIngestionType
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_configuration_assignment import GroupPolicyConfigurationAssignment
    from office365.common.group_policy_definition_value import GroupPolicyDefinitionValue


@version("beta")
class GroupPolicyConfiguration(Entity):
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

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="policyConfigurationIngestionType")
    @property
    def policy_configuration_ingestion_type(self) -> Optional[GroupPolicyConfigurationIngestionType]:
        """Gets the policyConfigurationIngestionType property"""
        return self.properties.get("policyConfigurationIngestionType", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[GroupPolicyConfigurationAssignment]:
        """Gets the assignments property"""
        from office365.common.group_policy_configuration_assignment import GroupPolicyConfigurationAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[GroupPolicyConfigurationAssignment](
                self.context, GroupPolicyConfigurationAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="definitionValues", navigation=True)
    @property
    def definition_values(self) -> EntityCollection[GroupPolicyDefinitionValue]:
        """Gets the definitionValues property"""
        from office365.common.group_policy_definition_value import GroupPolicyDefinitionValue

        return self.properties.get(
            "definitionValues",
            EntityCollection[GroupPolicyDefinitionValue](
                self.context, GroupPolicyDefinitionValue, ResourcePath("definitionValues", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyConfiguration"

    def assign(
        self, assignments: ClientValueCollection[GroupPolicyConfigurationAssignment]
    ) -> EntityCollection[GroupPolicyConfigurationAssignment]:
        """assign operation.

        Args:
            assignments (ClientValueCollection[GroupPolicyConfigurationAssignment]):
                assignments parameter
        """
        from office365.common.group_policy_configuration_assignment import GroupPolicyConfigurationAssignment

        return_type = EntityCollection(self.context, GroupPolicyConfigurationAssignment)
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def update_definition_values(
        self,
        added: ClientValueCollection[GroupPolicyDefinitionValue],
        updated: ClientValueCollection[GroupPolicyDefinitionValue],
        deleted_ids: list[str],
    ) -> Self:
        """updateDefinitionValues operation.

        Args:
            added (ClientValueCollection[GroupPolicyDefinitionValue]):
                added parameter
            updated (ClientValueCollection[GroupPolicyDefinitionValue]):
                updated parameter
            deleted_ids (list[str]):
                deletedIds parameter
        """
        qry = ServiceOperationQuery(
            self,
            "updateDefinitionValues",
            None,
            {"added": added, "updated": updated, "deletedIds": StringCollection(deleted_ids)},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
