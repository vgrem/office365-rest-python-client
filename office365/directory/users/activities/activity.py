from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.status import Status
from office365.directory.visual_info import VisualInfo
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class UserActivity(Entity):
    """
    Represents a single activity within an app - for example, a TV show, a document, or a current campaign
    in a video game. When a user engages with that activity, the engagement is captured as a history item
    that indicates the start and end time for that activity. As the user re-engages with that activity over time,
    multiple history items are recorded for a single user activity.
    """

    @odata(name="activationUrl")
    @property
    def activation_url(self) -> Optional[str]:
        """URL used to launch the activity in the best native experience represented by the appId.
        Might launch a web-based app if no native app exists
        """
        return self.properties.get("activationUrl", None)

    @odata(name="activitySourceHost")
    @property
    def activity_source_host(self) -> Optional[str]:
        """Required. URL for the domain representing the cross-platform identity mapping for the app.
        Mapping is stored either as a JSON file hosted on the domain or configurable via Windows Dev Center.
        The JSON file is named cross-platform-app-identifiers and is hosted at root of your HTTPS domain,
        either at the top level domain or include a sub domain.
        For example: https://contoso.com or https://myapp.contoso.com but NOT https://myapp.contoso.com/somepath.
        You must have a unique file and domain (or sub domain) per cross-platform app identity.
        For example, a separate file and domain is needed for Word vs. PowerPoint.
        """
        return self.properties.get("activitySourceHost", None)

    @odata(name="appActivityId")
    @property
    def app_activity_id(self) -> Optional[str]:
        """
        The unique activity ID in the context of the app - supplied by caller and immutable thereafter.
        """
        return self.properties.get("appActivityId", None)

    @odata(name="appDisplayName")
    @property
    def app_display_name(self) -> Optional[str]:
        """
        Short text description of the app used to generate the activity for use in cases when the app is
        not installed on the user’s local device.
        """
        return self.properties.get("appDisplayName", None)

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """Set by the server. DateTime in UTC when the object was created on the server."""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="expirationDateTime")
    @property
    def expiration_datetime(self) -> datetime:
        """Set by the server. DateTime in UTC when the object was created on the server."""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="historyItems", navigation=True)
    @property
    def history_items(self):
        """NavigationProperty/Containment; navigation property to the associated activity."""
        from office365.directory.users.activities.history_item import (
            ActivityHistoryItem,
        )

        return self.properties.get(
            "historyItems",
            EntityCollection(self.context, ActivityHistoryItem, ResourcePath("historyItems", self.resource_path)),
        )

    @odata(name="contentInfo")
    @property
    def content_info(self) -> Json:
        """Gets the contentInfo property"""
        return self.properties.get("contentInfo", Json())

    @odata(name="contentUrl")
    @property
    def content_url(self) -> Optional[str]:
        """Gets the contentUrl property"""
        return self.properties.get("contentUrl", None)

    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="fallbackUrl")
    @property
    def fallback_url(self) -> Optional[str]:
        """Gets the fallbackUrl property"""
        return self.properties.get("fallbackUrl", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="userTimezone")
    @property
    def user_timezone(self) -> Optional[str]:
        """Gets the userTimezone property"""
        return self.properties.get("userTimezone", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserActivity"

    @odata(name="status")
    @property
    def status(self) -> Status:
        """Gets the status property"""
        return self.properties.get("status", Status.active)

    @odata(name="visualElements")
    @property
    def visual_elements(self) -> VisualInfo:
        """Gets the visualElements property"""
        return self.properties.get("visualElements", VisualInfo())
