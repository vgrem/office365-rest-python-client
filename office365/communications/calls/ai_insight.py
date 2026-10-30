from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.calls.ai_insight_view_point import (
        CallAiInsightViewPoint,
    )
    from office365.copilot.action_item import ActionItem
    from office365.teams.teamwork.meeting_note import MeetingNote


class CallAiInsight(Entity):
    @odata(name="actionItems")
    @property
    def action_items(self) -> ClientValueCollection[ActionItem]:
        """Gets the actionItems property"""
        from office365.copilot.action_item import ActionItem

        return self.properties.get("actionItems", ClientValueCollection[ActionItem](ActionItem))

    @odata(name="callId")
    @property
    def call_id(self) -> Optional[str]:
        """Gets the callId property"""
        return self.properties.get("callId", None)

    @odata(name="contentCorrelationId")
    @property
    def content_correlation_id(self) -> Optional[str]:
        """Gets the contentCorrelationId property"""
        return self.properties.get("contentCorrelationId", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="meetingNotes")
    @property
    def meeting_notes(self) -> ClientValueCollection[MeetingNote]:
        """Gets the meetingNotes property"""
        from office365.teams.teamwork.meeting_note import MeetingNote

        return self.properties.get("meetingNotes", ClientValueCollection[MeetingNote](MeetingNote))

    @odata(name="viewpoint")
    @property
    def viewpoint(self) -> CallAiInsightViewPoint:
        """Gets the viewpoint property"""
        from office365.communications.calls.ai_insight_view_point import (
            CallAiInsightViewPoint,
        )

        return self.properties.get("viewpoint", CallAiInsightViewPoint())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallAiInsight"
