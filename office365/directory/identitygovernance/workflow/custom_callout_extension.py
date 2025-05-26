from typing import Optional

from office365.entity import Entity


class CustomCalloutExtension(Entity):
    """An abstract type that defines the configuration for apps that can extend the customer's identity flows."""

    @property
    def display_name(self):
        # type: () -> Optional[str]
        """Display name for the customCalloutExtension object."""
        return self.properties.get("displayName", None)
