from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MigrationPerformanceEntityData(Entity):
    """"""

    @odata(name="AgentId")
    @property
    def agent_id(self) -> Optional[UUID]:
        """Gets the AgentId property"""
        return self.properties.get("AgentId", None)

    @odata(name="AgentName")
    @property
    def agent_name(self) -> Optional[str]:
        """Gets the AgentName property"""
        return self.properties.get("AgentName", None)

    @odata(name="Bottleneck")
    @property
    def bottleneck(self) -> Optional[str]:
        """Gets the Bottleneck property"""
        return self.properties.get("Bottleneck", None)

    @odata(name="DiskWritingSpeed")
    @property
    def disk_writing_speed(self) -> Optional[int]:
        """Gets the DiskWritingSpeed property"""
        return self.properties.get("DiskWritingSpeed", None)

    @odata(name="Duration")
    @property
    def duration(self) -> Optional[int]:
        """Gets the Duration property"""
        return self.properties.get("Duration", None)

    @odata(name="MigratedBytes")
    @property
    def migrated_bytes(self) -> Optional[int]:
        """Gets the MigratedBytes property"""
        return self.properties.get("MigratedBytes", None)

    @odata(name="MigratedFiles")
    @property
    def migrated_files(self) -> Optional[int]:
        """Gets the MigratedFiles property"""
        return self.properties.get("MigratedFiles", None)

    @odata(name="PackingSpeed")
    @property
    def packing_speed(self) -> Optional[int]:
        """Gets the PackingSpeed property"""
        return self.properties.get("PackingSpeed", None)

    @odata(name="Recommendation")
    @property
    def recommendation(self) -> Optional[str]:
        """Gets the Recommendation property"""
        return self.properties.get("Recommendation", None)

    @odata(name="ResourceId")
    @property
    def resource_id(self) -> Optional[UUID]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)

    @odata(name="SourceReadingSpeed")
    @property
    def source_reading_speed(self) -> Optional[int]:
        """Gets the SourceReadingSpeed property"""
        return self.properties.get("SourceReadingSpeed", None)

    @odata(name="SPOProcessingSpeed")
    @property
    def spo_processing_speed(self) -> Optional[int]:
        """Gets the SPOProcessingSpeed property"""
        return self.properties.get("SPOProcessingSpeed", None)

    @odata(name="Timestamp")
    @property
    def timestamp(self) -> Optional[datetime]:
        """Gets the Timestamp property"""
        return self.properties.get("Timestamp", None)

    @odata(name="UploadingSpeed")
    @property
    def uploading_speed(self) -> Optional[int]:
        """Gets the UploadingSpeed property"""
        return self.properties.get("UploadingSpeed", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationPerformanceEntityData"
