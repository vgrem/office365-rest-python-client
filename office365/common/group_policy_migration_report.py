from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.common.group_policy_migration_readiness import GroupPolicyMigrationReadiness
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.group_policy_setting_mapping import GroupPolicySettingMapping
    from office365.common.unsupported_group_policy_extension import UnsupportedGroupPolicyExtension


@version("beta")
class GroupPolicyMigrationReport(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="groupPolicyCreatedDateTime")
    @property
    def group_policy_created_date_time(self) -> Optional[datetime]:
        """Gets the groupPolicyCreatedDateTime property"""
        return self.properties.get("groupPolicyCreatedDateTime", None)

    @odata(name="groupPolicyLastModifiedDateTime")
    @property
    def group_policy_last_modified_date_time(self) -> Optional[datetime]:
        """Gets the groupPolicyLastModifiedDateTime property"""
        return self.properties.get("groupPolicyLastModifiedDateTime", None)

    @odata(name="groupPolicyObjectId")
    @property
    def group_policy_object_id(self) -> Optional[UUID]:
        """Gets the groupPolicyObjectId property"""
        return self.properties.get("groupPolicyObjectId", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="migrationReadiness")
    @property
    def migration_readiness(self) -> Optional[GroupPolicyMigrationReadiness]:
        """Gets the migrationReadiness property"""
        return self.properties.get("migrationReadiness", None)

    @odata(name="ouDistinguishedName")
    @property
    def ou_distinguished_name(self) -> Optional[str]:
        """Gets the ouDistinguishedName property"""
        return self.properties.get("ouDistinguishedName", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="supportedSettingsCount")
    @property
    def supported_settings_count(self) -> Optional[int]:
        """Gets the supportedSettingsCount property"""
        return self.properties.get("supportedSettingsCount", None)

    @odata(name="supportedSettingsPercent")
    @property
    def supported_settings_percent(self) -> Optional[int]:
        """Gets the supportedSettingsPercent property"""
        return self.properties.get("supportedSettingsPercent", None)

    @odata(name="targetedInActiveDirectory")
    @property
    def targeted_in_active_directory(self) -> Optional[bool]:
        """Gets the targetedInActiveDirectory property"""
        return self.properties.get("targetedInActiveDirectory", None)

    @odata(name="totalSettingsCount")
    @property
    def total_settings_count(self) -> Optional[int]:
        """Gets the totalSettingsCount property"""
        return self.properties.get("totalSettingsCount", None)

    @odata(name="groupPolicySettingMappings", navigation=True)
    @property
    def group_policy_setting_mappings(self) -> EntityCollection[GroupPolicySettingMapping]:
        """Gets the groupPolicySettingMappings property"""
        from office365.common.group_policy_setting_mapping import GroupPolicySettingMapping

        return self.properties.get(
            "groupPolicySettingMappings",
            EntityCollection[GroupPolicySettingMapping](
                self.context, GroupPolicySettingMapping, ResourcePath("groupPolicySettingMappings", self.resource_path)
            ),
        )

    @odata(name="unsupportedGroupPolicyExtensions", navigation=True)
    @property
    def unsupported_group_policy_extensions(self) -> EntityCollection[UnsupportedGroupPolicyExtension]:
        """Gets the unsupportedGroupPolicyExtensions property"""
        from office365.common.unsupported_group_policy_extension import UnsupportedGroupPolicyExtension

        return self.properties.get(
            "unsupportedGroupPolicyExtensions",
            EntityCollection[UnsupportedGroupPolicyExtension](
                self.context,
                UnsupportedGroupPolicyExtension,
                ResourcePath("unsupportedGroupPolicyExtensions", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyMigrationReport"

    def update_scope_tags(self, role_scope_tag_ids: list[str]) -> ClientResult[str]:
        """updateScopeTags operation.

        Args:
            role_scope_tag_ids (list[str]):
                roleScopeTagIds parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "updateScopeTags", None, {"roleScopeTagIds": StringCollection(role_scope_tag_ids)}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
