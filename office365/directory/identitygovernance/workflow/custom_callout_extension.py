from typing import Optional

from office365.entity import Entity


class CustomCalloutExtension(Entity):
    """An abstract type that defines the configuration for apps that can extend the customer's identity flows."""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @property
    def display_name(self):
        # type: () -> Optional[str]
        """Display name for the customCalloutExtension object."""
        return self.properties.get("displayName", None)
