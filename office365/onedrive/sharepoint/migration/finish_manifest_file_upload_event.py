from __future__ import annotations

from typing import Optional

from office365.onedrive.sharepoint.migration.event import SharePointMigrationEvent
from office365.runtime.types.odata_property import odata


class SharePointMigrationFinishManifestFileUploadEvent(SharePointMigrationEvent):
    @odata(name="manifestFileName")
    @property
    def manifest_file_name(self) -> Optional[str]:
        """Gets the manifestFileName property"""
        return self.properties.get("manifestFileName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationFinishManifestFileUploadEvent"
