from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.outlook.calendar.email_address import EmailAddress
from office365.runtime.types.odata_property import odata, version


@version("beta")
class Mention(Entity):
    @odata(name="application")
    @property
    def application(self) -> Optional[str]:
        """Gets the application property"""
        return self.properties.get("application", None)

    @odata(name="clientReference")
    @property
    def client_reference(self) -> Optional[str]:
        """Gets the clientReference property"""
        return self.properties.get("clientReference", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> EmailAddress:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", EmailAddress())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deepLink")
    @property
    def deep_link(self) -> Optional[str]:
        """Gets the deepLink property"""
        return self.properties.get("deepLink", None)

    @odata(name="mentioned")
    @property
    def mentioned(self) -> EmailAddress:
        """Gets the mentioned property"""
        return self.properties.get("mentioned", EmailAddress())

    @odata(name="mentionText")
    @property
    def mention_text(self) -> Optional[str]:
        """Gets the mentionText property"""
        return self.properties.get("mentionText", None)

    @odata(name="serverCreatedDateTime")
    @property
    def server_created_date_time(self) -> Optional[datetime]:
        """Gets the serverCreatedDateTime property"""
        return self.properties.get("serverCreatedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Mention"
