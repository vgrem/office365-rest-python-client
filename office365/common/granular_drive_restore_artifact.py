from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class GranularDriveRestoreArtifact(Entity):
    @odata(name="directoryObjectId")
    @property
    def directory_object_id(self) -> Optional[str]:
        """Gets the directoryObjectId property"""
        return self.properties.get("directoryObjectId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GranularDriveRestoreArtifact"
