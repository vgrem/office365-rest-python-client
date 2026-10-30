from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.viva.learning.content import LearningContent

if TYPE_CHECKING:
    from office365.teams.viva.learning.courses.activity import LearningCourseActivity


class LearningProvider(Entity):
    """Represents an entity that holds the details about a learning provider in Viva learning."""

    @odata(name="learningContents", navigation=True)
    @property
    def learning_contents(self) -> EntityCollection[LearningContent]:
        """Learning catalog items for the provider."""
        return self.properties.get(
            "learningContents",
            EntityCollection(
                self.context,
                LearningContent,
                ResourcePath("learningContents", self.resource_path),
            ),
        )

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isCourseActivitySyncEnabled")
    @property
    def is_course_activity_sync_enabled(self) -> Optional[bool]:
        """Gets the isCourseActivitySyncEnabled property"""
        return self.properties.get("isCourseActivitySyncEnabled", None)

    @odata(name="loginWebUrl")
    @property
    def login_web_url(self) -> Optional[str]:
        """Gets the loginWebUrl property"""
        return self.properties.get("loginWebUrl", None)

    @odata(name="longLogoWebUrlForDarkTheme")
    @property
    def long_logo_web_url_for_dark_theme(self) -> Optional[str]:
        """Gets the longLogoWebUrlForDarkTheme property"""
        return self.properties.get("longLogoWebUrlForDarkTheme", None)

    @odata(name="longLogoWebUrlForLightTheme")
    @property
    def long_logo_web_url_for_light_theme(self) -> Optional[str]:
        """Gets the longLogoWebUrlForLightTheme property"""
        return self.properties.get("longLogoWebUrlForLightTheme", None)

    @odata(name="squareLogoWebUrlForDarkTheme")
    @property
    def square_logo_web_url_for_dark_theme(self) -> Optional[str]:
        """Gets the squareLogoWebUrlForDarkTheme property"""
        return self.properties.get("squareLogoWebUrlForDarkTheme", None)

    @odata(name="squareLogoWebUrlForLightTheme")
    @property
    def square_logo_web_url_for_light_theme(self) -> Optional[str]:
        """Gets the squareLogoWebUrlForLightTheme property"""
        return self.properties.get("squareLogoWebUrlForLightTheme", None)

    @odata(name="learningCourseActivities", navigation=True)
    @property
    def learning_course_activities(self) -> EntityCollection[LearningCourseActivity]:
        """Gets the learningCourseActivities property"""
        from office365.teams.viva.learning.courses.activity import (
            LearningCourseActivity,
        )

        return self.properties.get(
            "learningCourseActivities",
            EntityCollection[LearningCourseActivity](
                self.context, LearningCourseActivity, ResourcePath("learningCourseActivities", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LearningProvider"
