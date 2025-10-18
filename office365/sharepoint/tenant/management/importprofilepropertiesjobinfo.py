from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class ImportProfilePropertiesJobInfo(Entity):

    @property
    def error(self) -> Optional[int]:
        """Gets the Error property"""
        return self.properties.get("Error", None)

    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @property
    def log_folder_uri(self) -> Optional[str]:
        """Gets the LogFolderUri property"""
        return self.properties.get("LogFolderUri", None)

    @property
    def source_uri(self) -> Optional[str]:
        """Gets the SourceUri property"""
        return self.properties.get("SourceUri", None)

    @property
    def state(self) -> Optional[int]:
        """Gets the State property"""
        return self.properties.get("State", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantManagement.ImportProfilePropertiesJobInfo"
