from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.notificationtemplatebrandingoptions import NotificationTemplateBrandingOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.localized_notification_message import (
        LocalizedNotificationMessage,
    )


class NotificationMessageTemplate(Entity):
    @odata(name="brandingOptions")
    @property
    def branding_options(self) -> NotificationTemplateBrandingOptions:
        """Gets the brandingOptions property"""
        return self.properties.get("brandingOptions", NotificationTemplateBrandingOptions.none)

    @odata(name="defaultLocale")
    @property
    def default_locale(self) -> Optional[str]:
        """Gets the defaultLocale property"""
        return self.properties.get("defaultLocale", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="localizedNotificationMessages", navigation=True)
    @property
    def localized_notification_messages(self) -> EntityCollection[LocalizedNotificationMessage]:
        """Gets the localizedNotificationMessages property"""
        from office365.intune.devices.management.localized_notification_message import (
            LocalizedNotificationMessage,
        )

        return self.properties.get(
            "localizedNotificationMessages",
            EntityCollection[LocalizedNotificationMessage](
                self.context,
                LocalizedNotificationMessage,
                ResourcePath("localizedNotificationMessages", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NotificationMessageTemplate"
