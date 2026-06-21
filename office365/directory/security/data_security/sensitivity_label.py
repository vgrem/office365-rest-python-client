from typing import Optional

from office365.entity import Entity


class SensitivityLabel(Entity):
    """Represents a sensitivity label that defines how to protect and handle content."""

    @property
    def name(self) -> Optional[str]:
        return self.properties.get("name", None)

    @property
    def display_name(self) -> Optional[str]:
        return self.properties.get("displayName", None)

    @property
    def description(self) -> Optional[str]:
        return self.properties.get("description", None)

    @property
    def priority(self) -> Optional[int]:
        return self.properties.get("priority", None)

    @property
    def sensitivity(self) -> Optional[int]:
        return self.properties.get("sensitivity", None)

    @property
    def enabled(self) -> Optional[bool]:
        return self.properties.get("enabled", None)
