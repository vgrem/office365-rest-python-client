from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.question import AccessPackageQuestion
from office365.directory.identitygovernance.workflow.custom_extension_stage_setting import CustomExtensionStageSetting
from office365.directory.policies.allowedtargetscope import AllowedTargetScope
from office365.directory.subjectset import SubjectSet
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath


class AccessPackageAssignmentPolicy(Entity):
    @property
    def allowed_target_scope(self) -> AllowedTargetScope:
        """Gets the allowedTargetScope property"""
        return self.properties.get("allowedTargetScope", AllowedTargetScope.notSpecified)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def specific_allowed_targets(self) -> ClientValueCollection[SubjectSet]:
        """Gets the specificAllowedTargets property"""
        return self.properties.get("specificAllowedTargets", ClientValueCollection[SubjectSet](SubjectSet))

    @property
    def access_package(self) -> AccessPackage:
        """Gets the accessPackage property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import AccessPackage

        return self.properties.get(
            "accessPackage", AccessPackage(self.context, ResourcePath("accessPackage", self.resource_path))
        )

    @property
    def catalog(self) -> AccessPackageCatalog:
        """Gets the catalog property"""
        from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import (
            AccessPackageCatalog,
        )

        return self.properties.get(
            "catalog", AccessPackageCatalog(self.context, ResourcePath("catalog", self.resource_path))
        )

    @property
    def custom_extension_stage_settings(self) -> EntityCollection[CustomExtensionStageSetting]:
        """Gets the customExtensionStageSettings property"""
        return self.properties.get(
            "customExtensionStageSettings",
            EntityCollection[CustomExtensionStageSetting](
                self.context,
                CustomExtensionStageSetting,
                ResourcePath("customExtensionStageSettings", self.resource_path),
            ),
        )

    @property
    def questions(self) -> EntityCollection[AccessPackageQuestion]:
        """Gets the questions property"""
        return self.properties.get(
            "questions",
            EntityCollection[AccessPackageQuestion](
                self.context, AccessPackageQuestion, ResourcePath("questions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentPolicy"
