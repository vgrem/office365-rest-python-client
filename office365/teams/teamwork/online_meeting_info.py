from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.user_identity import TeamworkUserIdentity


@dataclass
class TeamworkOnlineMeetingInfo(ClientValue):
    """Represents details about an online meeting in Microsoft Teams.

    :param calendar_event_id: The identifier of the calendar event associated with the meeting.
    :param join_web_url: The URL that users click to join or uniquely identify the meeting.
    :param organizer: The organizer associated with the meeting.
    """

    calendarEventId: str | None = None
    joinWebUrl: str | None = None
    organizer: TeamworkUserIdentity = field(default_factory=TeamworkUserIdentity)
