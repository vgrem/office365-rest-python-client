from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity


class CallRecording(Entity):
    """Represents a recording associated with an online meeting."""

    @property
    def call_id(self):
        """The unique identifier for the call that is related to this recording. Read-only."""
        return self.properties.get("callId", None)

    @property
    def content(self) -> bytes | None:
        """Gets the content property"""
        return self.properties.get("content", None)

    @property
    def content_correlation_id(self) -> Optional[str]:
        """Gets the contentCorrelationId property"""
        return self.properties.get("contentCorrelationId", None)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @property
    def meeting_id(self) -> Optional[str]:
        """Gets the meetingId property"""
        return self.properties.get("meetingId", None)

    @property
    def meeting_organizer(self) -> IdentitySet:
        """Gets the meetingOrganizer property"""
        return self.properties.get("meetingOrganizer", IdentitySet())

    @property
    def recording_content_url(self) -> Optional[str]:
        """Gets the recordingContentUrl property"""
        return self.properties.get("recordingContentUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallRecording"
