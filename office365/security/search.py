from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Search(Entity):
    @odata(name="contentQuery")
    @property
    def content_query(self) -> Optional[str]:
        """Gets the contentQuery property"""
        return self.properties.get("contentQuery", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.Search"
