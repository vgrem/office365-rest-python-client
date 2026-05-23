from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.management.externalusers.collection import (
    ExternalUserCollection,
)


class GetExternalUsersResults(Entity):
    @property
    def total_user_count(self) -> Optional[int]:
        return self.properties.get("TotalUserCount", None)

    @property
    def user_collection_position(self) -> Optional[int]:
        return self.properties.get("UserCollectionPosition", None)

    @property
    def external_user_collection(self) -> ExternalUserCollection:
        return self.properties.get(
            "ExternalUserCollection",
            ExternalUserCollection(self.context, ResourcePath("ExternalUserCollection")),
        )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantManagement.GetExternalUsersResults"
