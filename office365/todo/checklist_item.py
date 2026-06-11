from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ChecklistItem(Entity):
    """Represents a subtask in a bigger todoTask. ChecklistItem allows breaking down a complex task into more
    actionable, smaller tasks."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self) -> Optional[str]:
        """Indicates the title of the checklistItem."""
        return self.properties.get("displayName", None)

    @odata(name="checkedDateTime")
    @property
    def checked_date_time(self) -> Optional[datetime]:
        """The date and time when the checklistItem was checked."""
        return self.properties.get("checkedDateTime", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """The date and time when the checklistItem was created."""
        return self.properties.get("createdDateTime", None)

    @odata(name="isChecked")
    @property
    def is_checked(self) -> Optional[bool]:
        """Indicates whether the checklistItem is checked."""
        return self.properties.get("isChecked", None)

    @property
    def entity_type_name(self) -> str:
        return None  # type: ignore
