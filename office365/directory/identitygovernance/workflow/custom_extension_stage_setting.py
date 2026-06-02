from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.customextensionstage import (
    AccessPackageCustomExtensionStage,
)
from office365.directory.identitygovernance.workflow.custom_callout_extension import CustomCalloutExtension
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class CustomExtensionStageSetting(Entity):
    @property
    def stage(self) -> AccessPackageCustomExtensionStage:
        """Gets the stage property"""
        return self.properties.get("stage", AccessPackageCustomExtensionStage.assignmentRequestCreated)

    @property
    def custom_extension(self) -> CustomCalloutExtension:
        """Gets the customExtension property"""
        return self.properties.get(
            "customExtension", CustomCalloutExtension(self.context, ResourcePath("customExtension", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomExtensionStageSetting"
