from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MigrationCredential(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationCredential"

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="LastModifiedBy")
    @property
    def last_modified_by(self) -> Optional[str]:
        """Gets the LastModifiedBy property"""
        return self.properties.get("LastModifiedBy", None)

    @odata(name="LastModifiedDateTimeUtc")
    @property
    def last_modified_datetime_utc(self) -> Optional[datetime]:
        """Gets the LastModifiedDateTimeUtc property"""
        return self.properties.get("LastModifiedDateTimeUtc", datetime.min)
