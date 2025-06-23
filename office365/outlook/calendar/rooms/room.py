from typing import Optional

from office365.outlook.calendar.place import Place


class Room(Place):
    """
    Represents a room in a tenant.
    In Exchange Online, each room is associated with a room mailbox. Derived from place.
    """

    @property
    def audio_device_name(self) -> Optional[str]:
        """Specifies the name of the audio device in the room."""
        return self.properties.get("audioDeviceName", None)

    @property
    def building(self) -> Optional[str]:
        """Specifies the building name or building number that the room is in."""
        return self.properties.get("building", None)
