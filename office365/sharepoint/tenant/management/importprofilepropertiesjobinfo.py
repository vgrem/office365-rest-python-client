from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ImportProfilePropertiesJobInfo(Entity):
    @odata(name="Error")
    @property
    def error(self) -> Optional[int]:
        """Gets the Error property"""
        return self.properties.get("Error", None)

    @odata(name="ErrorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="JobId")
    @property
    def job_id(self) -> Optional[UUID]:
        """Gets the JobId property"""
        return self.properties.get("JobId", None)

    @odata(name="LogFolderUri")
    @property
    def log_folder_uri(self) -> Optional[str]:
        """Gets the LogFolderUri property"""
        return self.properties.get("LogFolderUri", None)

    @odata(name="SourceUri")
    @property
    def source_uri(self) -> Optional[str]:
        """Gets the SourceUri property"""
        return self.properties.get("SourceUri", None)

    @odata(name="State")
    @property
    def state(self) -> Optional[int]:
        """Gets the State property"""
        return self.properties.get("State", None)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantManagement.ImportProfilePropertiesJobInfo"
