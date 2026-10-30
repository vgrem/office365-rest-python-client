from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identity_set import IdentitySet
    from office365.directory.protection.unitsbulkjobstatus import (
        ProtectionUnitsBulkJobStatus,
    )
    from office365.runtime.types.public_error import PublicError


class ProtectionUnitsBulkJobBase(Entity):
    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        from office365.runtime.types.public_error import PublicError

        return self.properties.get("error", PublicError())

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> ProtectionUnitsBulkJobStatus:
        """Gets the status property"""
        from office365.directory.protection.unitsbulkjobstatus import (
            ProtectionUnitsBulkJobStatus,
        )

        return self.properties.get("status", ProtectionUnitsBulkJobStatus.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProtectionUnitsBulkJobBase"
