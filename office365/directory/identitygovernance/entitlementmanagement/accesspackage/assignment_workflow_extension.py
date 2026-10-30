from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.extensions.custom.callbackconfiguration import CustomExtensionCallbackConfiguration
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AccessPackageAssignmentWorkflowExtension(Entity):
    @odata(name="callbackConfiguration")
    @property
    def callback_configuration(self) -> CustomExtensionCallbackConfiguration:
        """Gets the callbackConfiguration property"""
        return self.properties.get("callbackConfiguration", CustomExtensionCallbackConfiguration())

    @odata(name="createdBy")
    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> Optional[str]:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentWorkflowExtension"
