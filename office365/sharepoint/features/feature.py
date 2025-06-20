from typing import Optional

from office365.sharepoint.entity import Entity


class Feature(Entity):
    """Represents an activated feature."""

    @property
    def definition_id(self) -> Optional[str]:
        """Gets the GUID that identifies this feature."""
        return self.properties.get("DefinitionId", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the GUID that identifies this feature."""
        return self.properties.get("DisplayName", None)
