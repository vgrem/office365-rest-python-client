from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.backuprestore.notification_events_type import NotificationEventsType
    from office365.directory.rolemanagement.unifiedrole.notification_recipients import (
        NotificationRecipients,
    )


class EmailNotificationsSetting(Entity):
    @odata(name="additionalEvents")
    @property
    def additional_events(self) -> NotificationEventsType:
        """Gets the additionalEvents property"""
        from office365.backuprestore.notification_events_type import (
            NotificationEventsType,
        )

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
        from office365.directory.rolemanagement.unifiedrole.notification_recipients import (
            NotificationRecipients,
        )

        return self.properties.get("recipients", NotificationRecipients())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailNotificationsSetting"
