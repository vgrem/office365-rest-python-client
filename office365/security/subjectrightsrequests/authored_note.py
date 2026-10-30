from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity import Identity
from office365.entity import Entity
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.types.odata_property import odata


class AuthoredNote(Entity):
    @odata(name="author")
    @property
    def author(self) -> Identity:
        """Gets the author property"""
        return self.properties.get("author", Identity())

    @odata(name="content")
    @property
    def content(self) -> ItemBody:
        """Gets the content property"""
        return self.properties.get("content", ItemBody())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthoredNote"
