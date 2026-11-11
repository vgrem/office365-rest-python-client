from __future__ import annotations

from office365.runtime.types.odata_property import key, odata
from office365.sharepoint.entity import Entity


@key("DefinitionId")
class Feature(Entity):
    """Represents an activated feature."""

    @odata(name="DefinitionId")
    @property
    def definition_id(self) -> str | None:
        """The GUID that identifies this feature."""
        return self.properties.get("DefinitionId", None)

    @odata(name="DisplayName")
    @property
    def display_name(self) -> str | None:
        """The display name of this feature."""
        return self.properties.get("DisplayName", None)
