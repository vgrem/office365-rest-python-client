from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class LocalizedNotificationMessage(Entity):
    @odata(name="isDefault")
    @property
    def is_default(self) -> Optional[bool]:
        """Gets the isDefault property"""
        return self.properties.get("isDefault", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="locale")
    @property
    def locale(self) -> Optional[str]:
        """Gets the locale property"""
        return self.properties.get("locale", None)

    @odata(name="messageTemplate")
    @property
    def message_template(self) -> Optional[str]:
        """Gets the messageTemplate property"""
        return self.properties.get("messageTemplate", None)

    @odata(name="subject")
    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LocalizedNotificationMessage"
