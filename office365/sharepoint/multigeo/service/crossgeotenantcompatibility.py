from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossGeoTenantCompatibility(Entity):
    @odata(name="AbsCredentialsCount")
    @property
    def abs_credentials_count(self) -> Optional[int]:
        """Gets the AbsCredentialsCount property"""
        return self.properties.get("AbsCredentialsCount", None)

    @odata(name="BackupRestoreCompatibleDBSchemaVersion")
    @property
    def backup_restore_compatible_db_schema_version(self) -> Optional[str]:
        """Gets the BackupRestoreCompatibleDBSchemaVersion property"""
        return self.properties.get("BackupRestoreCompatibleDBSchemaVersion", None)

    @odata(name="DbExtensionSchemaNames")
    @property
    def db_extension_schema_names(self) -> Optional[StringCollection]:
        """Gets the DbExtensionSchemaNames property"""
        return self.properties.get("DbExtensionSchemaNames", None)

    @odata(name="DbExtensionSchemaVersions")
    @property
    def db_extension_schema_versions(self) -> Optional[StringCollection]:
        """Gets the DbExtensionSchemaVersions property"""
        return self.properties.get("DbExtensionSchemaVersions", None)

    @odata(name="DBSchemaSHA512Hash")
    @property
    def db_schema_sha512_hash(self) -> Optional[str]:
        """Gets the DBSchemaSHA512Hash property"""
        return self.properties.get("DBSchemaSHA512Hash", None)

    @odata(name="DbSchemaVersion")
    @property
    def db_schema_version(self) -> Optional[str]:
        """Gets the DbSchemaVersion property"""
        return self.properties.get("DbSchemaVersion", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantCompatibility"
