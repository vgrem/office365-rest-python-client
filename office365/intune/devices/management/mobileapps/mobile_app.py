from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.mobileapps.mobile_app_category import MobileAppCategory
from office365.intune.devices.management.mobileapps.publishingstate import MobileAppPublishingState
from office365.runtime.paths.resource_path import ResourcePath


class MobileApp(Entity):
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def developer(self) -> Optional[str]:
        """Gets the developer property"""
        return self.properties.get("developer", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def information_url(self) -> Optional[str]:
        """Gets the informationUrl property"""
        return self.properties.get("informationUrl", None)

    @property
    def is_featured(self) -> Optional[bool]:
        """Gets the isFeatured property"""
        return self.properties.get("isFeatured", None)

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def notes(self) -> Optional[str]:
        """Gets the notes property"""
        return self.properties.get("notes", None)

    @property
    def owner(self) -> Optional[str]:
        """Gets the owner property"""
        return self.properties.get("owner", None)

    @property
    def privacy_information_url(self) -> Optional[str]:
        """Gets the privacyInformationUrl property"""
        return self.properties.get("privacyInformationUrl", None)

    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @property
    def publishing_state(self) -> MobileAppPublishingState:
        """Gets the publishingState property"""
        return self.properties.get("publishingState", MobileAppPublishingState.notPublished)

    @property
    def categories(self) -> EntityCollection[MobileAppCategory]:
        """Gets the categories property"""
        return self.properties.get(
            "categories",
            EntityCollection[MobileAppCategory](
                self.context, MobileAppCategory, ResourcePath("categories", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileApp"
