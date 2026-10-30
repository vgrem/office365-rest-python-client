from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.onedrive.share_point_migration_job_error_level import SharePointMigrationJobErrorLevel
from office365.onedrive.share_point_migration_object_type import SharePointMigrationObjectType
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.public_error import PublicError


class SharePointMigrationJobErrorEvent(Entity):
    @odata(name="objectId")
    @property
    def object_id(self) -> Optional[str]:
        """Gets the objectId property"""
        return self.properties.get("objectId", None)

    @odata(name="objectUrl")
    @property
    def object_url(self) -> Optional[str]:
        """Gets the objectUrl property"""
        return self.properties.get("objectUrl", None)

    @odata(name="totalRetryCount")
    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobErrorEvent"

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        from office365.runtime.types.public_error import PublicError

        return self.properties.get("error", PublicError())

    @odata(name="errorLevel")
    @property
    def error_level(self) -> SharePointMigrationJobErrorLevel:
        """Gets the errorLevel property"""
        return self.properties.get("errorLevel", SharePointMigrationJobErrorLevel.important)

    @odata(name="objectType")
    @property
    def object_type(self) -> SharePointMigrationObjectType:
        """Gets the objectType property"""
        return self.properties.get("objectType", SharePointMigrationObjectType.site)
