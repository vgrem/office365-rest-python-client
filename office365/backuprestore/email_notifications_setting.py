from __future__ import annotations

from typing import Optional

from office365.backuprestore.notification_events_type import NotificationEventsType
from office365.directory.rolemanagement.unifiedrole.notification_recipients import NotificationRecipients
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class EmailNotificationsSetting(Entity):
    @odata(name="additionalEvents")
    @property
    def additional_events(self) -> NotificationEventsType:
        """Gets the additionalEvents property"""
        return self.properties.get("additionalEvents", NotificationEventsType.none)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="recipients")
    @property
    def recipients(self) -> NotificationRecipients:
        """Gets the recipients property"""
        return self.properties.get("recipients", NotificationRecipients())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailNotificationsSetting"
