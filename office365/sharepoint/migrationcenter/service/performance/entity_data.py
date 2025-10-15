from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class MigrationPerformanceEntityData(Entity):
    """"""

    @property
    def agent_id(self) -> Optional[UUID]:
        """Gets the AgentId property"""
        return self.properties.get("AgentId", None)

    @property
    def agent_name(self) -> Optional[str]:
        """Gets the AgentName property"""
        return self.properties.get("AgentName", None)

    @property
    def bottleneck(self) -> Optional[str]:
        """Gets the Bottleneck property"""
        return self.properties.get("Bottleneck", None)

    @property
    def disk_writing_speed(self) -> Optional[int]:
        """Gets the DiskWritingSpeed property"""
        return self.properties.get("DiskWritingSpeed", None)

    @property
    def duration(self) -> Optional[int]:
        """Gets the Duration property"""
        return self.properties.get("Duration", None)

    @property
    def migrated_bytes(self) -> Optional[int]:
        """Gets the MigratedBytes property"""
        return self.properties.get("MigratedBytes", None)

    @property
    def migrated_files(self) -> Optional[int]:
        """Gets the MigratedFiles property"""
        return self.properties.get("MigratedFiles", None)

    @property
    def packing_speed(self) -> Optional[int]:
        """Gets the PackingSpeed property"""
        return self.properties.get("PackingSpeed", None)

    @property
    def recommendation(self) -> Optional[str]:
        """Gets the Recommendation property"""
        return self.properties.get("Recommendation", None)

    @property
    def resource_id(self) -> Optional[UUID]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)

    @property
    def source_reading_speed(self) -> Optional[int]:
        """Gets the SourceReadingSpeed property"""
        return self.properties.get("SourceReadingSpeed", None)

    @property
    def spo_processing_speed(self) -> Optional[int]:
        """Gets the SPOProcessingSpeed property"""
        return self.properties.get("SPOProcessingSpeed", None)

    @property
    def timestamp(self) -> datetime:
        """Gets the Timestamp property"""
        return self.properties.get("Timestamp", None)

    @property
    def uploading_speed(self) -> Optional[int]:
        """Gets the UploadingSpeed property"""
        return self.properties.get("UploadingSpeed", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationPerformanceEntityData"
