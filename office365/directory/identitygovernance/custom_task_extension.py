from __future__ import annotations

from datetime import datetime

from office365.directory.extensions.customextensioncallbackconfiguration import CustomExtensionCallbackConfiguration
from office365.directory.users.user import User
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class CustomTaskExtension(Entity):
    @property
    def callback_configuration(self) -> CustomExtensionCallbackConfiguration:
        """Gets the callbackConfiguration property"""
        return self.properties.get("callbackConfiguration", CustomExtensionCallbackConfiguration())

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def created_by(self) -> User:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", User(self.context, ResourcePath("createdBy", self.resource_path)))

    @property
    def last_modified_by(self) -> User:
        """Gets the lastModifiedBy property"""
        return self.properties.get(
            "lastModifiedBy", User(self.context, ResourcePath("lastModifiedBy", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CustomTaskExtension"
