from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.duration import timedelta
    from office365.teams.viva.learning.level import Level


class LearningContent(Entity):
    """Represents the metadata of content for employee learning."""

    @odata(name="additionalTags")
    @property
    def additional_tags(self) -> StringCollection:
        """Gets the additionalTags property"""
        return self.properties.get("additionalTags", StringCollection())

    @odata(name="contentWebUrl")
    @property
    def content_web_url(self) -> Optional[str]:
        """Gets the contentWebUrl property"""
        return self.properties.get("contentWebUrl", None)

    @odata(name="contributors")
    @property
    def contributors(self) -> StringCollection:
        """Gets the contributors property"""
        return self.properties.get("contributors", StringCollection())

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

    @odata(name="duration")
    @property
    def duration(self) -> Optional[timedelta]:
        """Gets the duration property"""
        return self.properties.get("duration", None)

    @odata(name="externalId")
    @property
    def external_id(self) -> Optional[str]:
        """Gets the externalId property"""
        return self.properties.get("externalId", None)

    @odata(name="format")
    @property
    def format(self) -> Optional[str]:
        """Gets the format property"""
        return self.properties.get("format", None)

    @odata(name="isActive")
    @property
    def is_active(self) -> Optional[bool]:
        """Gets the isActive property"""
        return self.properties.get("isActive", None)

    @odata(name="isPremium")
    @property
    def is_premium(self) -> Optional[bool]:
        """Gets the isPremium property"""
        return self.properties.get("isPremium", None)

    @odata(name="isSearchable")
    @property
    def is_searchable(self) -> Optional[bool]:
        """Gets the isSearchable property"""
        return self.properties.get("isSearchable", None)

    @odata(name="languageTag")
    @property
    def language_tag(self) -> Optional[str]:
        """Gets the languageTag property"""
        return self.properties.get("languageTag", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="level")
    @property
    def level(self) -> Level:
        """Gets the level property"""
        from office365.teams.viva.learning.level import Level

        return self.properties.get("level", Level.beginner)

    @odata(name="numberOfPages")
    @property
    def number_of_pages(self) -> Optional[int]:
        """Gets the numberOfPages property"""
        return self.properties.get("numberOfPages", None)

    @odata(name="skillTags")
    @property
    def skill_tags(self) -> StringCollection:
        """Gets the skillTags property"""
        return self.properties.get("skillTags", StringCollection())

    @odata(name="sourceName")
    @property
    def source_name(self) -> Optional[str]:
        """Gets the sourceName property"""
        return self.properties.get("sourceName", None)

    @odata(name="thumbnailWebUrl")
    @property
    def thumbnail_web_url(self) -> Optional[str]:
        """Gets the thumbnailWebUrl property"""
        return self.properties.get("thumbnailWebUrl", None)

    @odata(name="title")
    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LearningContent"
