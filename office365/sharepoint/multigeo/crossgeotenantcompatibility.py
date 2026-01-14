from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class CrossGeoTenantCompatibility(Entity):
    @property
    def abs_credentials_count(self) -> Optional[int]:
        """Gets the AbsCredentialsCount property"""
        return self.properties.get("AbsCredentialsCount", None)

    @property
    def backup_restore_compatible_db_schema_version(self) -> Optional[str]:
        """Gets the BackupRestoreCompatibleDBSchemaVersion property"""
        return self.properties.get("BackupRestoreCompatibleDBSchemaVersion", None)

    @property
    def db_extension_schema_names(self) -> StringCollection:
        """Gets the DbExtensionSchemaNames property"""
        return self.properties.get("DbExtensionSchemaNames", None)

    @property
    def db_extension_schema_versions(self) -> StringCollection:
        """Gets the DbExtensionSchemaVersions property"""
        return self.properties.get("DbExtensionSchemaVersions", None)

    @property
    def db_schema_sha512_hash(self) -> Optional[str]:
        """Gets the DBSchemaSHA512Hash property"""
        return self.properties.get("DBSchemaSHA512Hash", None)

    @property
    def db_schema_version(self) -> Optional[str]:
        """Gets the DbSchemaVersion property"""
        return self.properties.get("DbSchemaVersion", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossGeoTenantCompatibility"
