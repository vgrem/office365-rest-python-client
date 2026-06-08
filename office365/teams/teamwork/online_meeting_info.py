from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.user_identity import TeamworkUserIdentity


@dataclass
class TeamworkOnlineMeetingInfo(ClientValue):
    """Represents details about an online meeting in Microsoft Teams.

    Args:
        calendar_event_id: The identifier of the calendar event associated with the meeting.
        join_web_url: The URL that users click to join or uniquely identify the meeting.
        organizer: The organizer associated with the meeting.
    """

    calendarEventId: str | None = None
    joinWebUrl: str | None = None
    organizer: TeamworkUserIdentity = field(default_factory=TeamworkUserIdentity)
