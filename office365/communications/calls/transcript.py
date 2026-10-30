from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class CallTranscript(Entity):
    """Represents a transcript associated with an online meeting."""

    @odata(name="callId")
    @property
    def call_id(self) -> Optional[str]:
        """Gets the callId property"""
        return self.properties.get("callId", None)

    @odata(name="content")
    @property
    def content(self) -> bytes | None:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="contentCorrelationId")
    @property
    def content_correlation_id(self) -> Optional[str]:
        """Gets the contentCorrelationId property"""
        return self.properties.get("contentCorrelationId", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="meetingId")
    @property
    def meeting_id(self) -> Optional[str]:
        """Gets the meetingId property"""
        return self.properties.get("meetingId", None)

    @odata(name="meetingOrganizer")
    @property
    def meeting_organizer(self) -> IdentitySet:
        """Gets the meetingOrganizer property"""
        return self.properties.get("meetingOrganizer", IdentitySet())

    @odata(name="metadataContent")
    @property
    def metadata_content(self) -> bytes | None:
        """Gets the metadataContent property"""
        return self.properties.get("metadataContent", None)

    @odata(name="transcriptContentUrl")
    @property
    def transcript_content_url(self) -> Optional[str]:
        """Gets the transcriptContentUrl property"""
        return self.properties.get("transcriptContentUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallTranscript"
