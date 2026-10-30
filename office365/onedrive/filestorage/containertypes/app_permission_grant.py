from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.onedrive.filestorage.containertypes.app_permission import FileStorageContainerTypeAppPermission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import key, odata


@key("appId")
class FileStorageContainerTypeAppPermissionGrant(Entity):
    @odata(name="appId")
    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @odata(name="applicationPermissions")
    @property
    def application_permissions(self) -> ClientValueCollection[FileStorageContainerTypeAppPermission]:
        """Gets the applicationPermissions property"""
        return self.properties.get(
            "applicationPermissions",
            ClientValueCollection[FileStorageContainerTypeAppPermission](FileStorageContainerTypeAppPermission),
        )

    @odata(name="delegatedPermissions")
    @property
    def delegated_permissions(self) -> ClientValueCollection[FileStorageContainerTypeAppPermission]:
        """Gets the delegatedPermissions property"""
        return self.properties.get(
            "delegatedPermissions",
            ClientValueCollection[FileStorageContainerTypeAppPermission](FileStorageContainerTypeAppPermission),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerTypeAppPermissionGrant"
