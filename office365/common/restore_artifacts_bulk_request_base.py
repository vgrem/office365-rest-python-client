from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.backuprestore.destinationtype import DestinationType
    from office365.backuprestore.restoreartifactsbulkrequeststatus import (
        RestoreArtifactsBulkRequestStatus,
    )
    from office365.backuprestore.restorepoints.preference import RestorePointPreference
    from office365.backuprestore.restorepoints.tags import RestorePointTags
    from office365.backuprestore.time_period import TimePeriod
    from office365.directory.identity_set import IdentitySet
    from office365.runtime.types.public_error import PublicError


class RestoreArtifactsBulkRequestBase(Entity):
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

    @odata(name="destinationType")
    @property
    def destination_type(self) -> DestinationType:
        """Gets the destinationType property"""
        from office365.backuprestore.destinationtype import DestinationType

        return self.properties.get("destinationType", DestinationType.new)

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

    @odata(name="protectionTimePeriod")
    @property
    def protection_time_period(self) -> TimePeriod:
        """Gets the protectionTimePeriod property"""
        from office365.backuprestore.time_period import TimePeriod

        return self.properties.get("protectionTimePeriod", TimePeriod())

    @odata(name="protectionUnitIds")
    @property
    def protection_unit_ids(self) -> StringCollection:
        """Gets the protectionUnitIds property"""
        return self.properties.get("protectionUnitIds", StringCollection())

    @odata(name="restorePointPreference")
    @property
    def restore_point_preference(self) -> RestorePointPreference:
        """Gets the restorePointPreference property"""
        from office365.backuprestore.restorepoints.preference import (
            RestorePointPreference,
        )

        return self.properties.get("restorePointPreference", RestorePointPreference.latest)

    @odata(name="status")
    @property
    def status(self) -> RestoreArtifactsBulkRequestStatus:
        """Gets the status property"""
        from office365.backuprestore.restoreartifactsbulkrequeststatus import (
            RestoreArtifactsBulkRequestStatus,
        )

        return self.properties.get("status", RestoreArtifactsBulkRequestStatus.unknown)

    @odata(name="tags")
    @property
    def tags(self) -> RestorePointTags:
        """Gets the tags property"""
        from office365.backuprestore.restorepoints.tags import RestorePointTags

        return self.properties.get("tags", RestorePointTags.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestoreArtifactsBulkRequestBase"
