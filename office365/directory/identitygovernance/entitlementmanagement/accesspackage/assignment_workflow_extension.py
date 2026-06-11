from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.extensions.custom.callbackconfiguration import CustomExtensionCallbackConfiguration
from office365.entity import Entity


class AccessPackageAssignmentWorkflowExtension(Entity):
    @property
    def callback_configuration(self) -> CustomExtensionCallbackConfiguration:
        """Gets the callbackConfiguration property"""
        return self.properties.get("callbackConfiguration", CustomExtensionCallbackConfiguration())

    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def last_modified_by(self) -> Optional[str]:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", None)

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentWorkflowExtension"
