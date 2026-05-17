from typing import Optional

from office365.entity import Entity


class OnlineMeetingBase(Entity):
    """Represents a base online meeting. The base type of onlineMeeting and virtualEventSession."""

    @property
    def allow_attendee_to_enable_camera(self) -> Optional[bool]:
        """Indicates whether attendees can turn on their camera."""
        return self.properties.get("allowAttendeeToEnableCamera", None)

    @property
    def allow_attendee_to_enable_mic(self) -> Optional[bool]:
        """Indicates whether attendees can turn on their microphone."""
        return self.properties.get("allowAttendeeToEnableMic", None)

    @property
    def allow_breakout_rooms(self) -> Optional[bool]:
        """Indicates whether breakout rooms are enabled for the meeting."""
        return self.properties.get("allowBreakoutRooms", None)
