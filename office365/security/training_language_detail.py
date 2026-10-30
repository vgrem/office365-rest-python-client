from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.email_identity import EmailIdentity
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TrainingLanguageDetail(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[str]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> EmailIdentity:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", EmailIdentity())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isDefaultLangauge")
    @property
    def is_default_langauge(self) -> Optional[bool]:
        """Gets the isDefaultLangauge property"""
        return self.properties.get("isDefaultLangauge", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> EmailIdentity:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", EmailIdentity())

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TrainingLanguageDetail"
