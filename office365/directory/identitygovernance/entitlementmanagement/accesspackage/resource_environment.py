from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.connection_info import ConnectionInfo
    from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource import (
        AccessPackageResource,
    )


class AccessPackageResourceEnvironment(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
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

    @odata(name="isDefaultEnvironment")
    @property
    def is_default_environment(self) -> Optional[bool]:
        """Gets the isDefaultEnvironment property"""
        return self.properties.get("isDefaultEnvironment", None)

    @odata(name="modifiedDateTime")
    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @odata(name="originId")
    @property
    def origin_id(self) -> Optional[str]:
        """Gets the originId property"""
        return self.properties.get("originId", None)

    @odata(name="originSystem")
    @property
    def origin_system(self) -> Optional[str]:
        """Gets the originSystem property"""
        return self.properties.get("originSystem", None)

    @odata(name="resources", navigation=True)
    @property
    def resources(self) -> EntityCollection[AccessPackageResource]:
        """Gets the resources property"""
        return self.properties.get(
            "resources",
            EntityCollection[AccessPackageResource](
                self.context, AccessPackageResource, ResourcePath("resources", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceEnvironment"

    @odata(name="connectionInfo")
    @property
    def connection_info(self) -> ConnectionInfo:
        """Gets the connectionInfo property"""
        from office365.directory.connection_info import ConnectionInfo

        return self.properties.get("connectionInfo", ConnectionInfo())
