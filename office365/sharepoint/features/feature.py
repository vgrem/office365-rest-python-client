from __future__ import annotations

from office365.sharepoint.entity import Entity


class Feature(Entity):
    """Represents an activated feature."""

    @property
    def definition_id(self) -> str | None:
        """The GUID that identifies this feature."""
        return self.properties.get("DefinitionId", None)

    @property
    def display_name(self) -> str | None:
        """The display name of this feature."""
        return self.properties.get("DisplayName", None)

    @property
    def property_ref_name(self) -> str:
        return "DefinitionId"
