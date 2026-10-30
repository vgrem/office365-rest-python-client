from __future__ import annotations

from datetime import datetime

from office365.directory.extensions.custom.callbackconfiguration import (
    CustomExtensionCallbackConfiguration,
)
from office365.directory.identitygovernance.custom_task_extension_reply_mode import CustomTaskExtensionReplyMode
from office365.directory.users.user import User
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class CustomTaskExtension(Entity):
    @odata(name="callbackConfiguration")
    @property
    def callback_configuration(self) -> CustomExtensionCallbackConfiguration:
        """Gets the callbackConfiguration property"""
        return self.properties.get("callbackConfiguration", CustomExtensionCallbackConfiguration())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="createdBy", navigation=True)
    @property
    def created_by(self) -> User:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", User(self.context, ResourcePath("createdBy", self.resource_path)))

    @odata(name="lastModifiedBy", navigation=True)
    @property
    def last_modified_by(self) -> User:
        """Gets the lastModifiedBy property"""
        return self.properties.get(
            "lastModifiedBy", User(self.context, ResourcePath("lastModifiedBy", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CustomTaskExtension"

    @odata(name="replyMode")
    @property
    def reply_mode(self) -> CustomTaskExtensionReplyMode:
        """Gets the replyMode property"""
        return self.properties.get("replyMode", CustomTaskExtensionReplyMode.none)
