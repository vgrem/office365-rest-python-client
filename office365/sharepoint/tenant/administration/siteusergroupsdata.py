from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.user_info import UserInfo


@dataclass
class SiteUserGroupsData(ClientValue):
    members: ClientValueCollection[UserInfo] = field(default_factory=lambda: ClientValueCollection(UserInfo))
    owners: ClientValueCollection[UserInfo] = field(default_factory=lambda: ClientValueCollection(UserInfo))
    siteId: UUID | None = None
    visitors: ClientValueCollection[UserInfo] = field(default_factory=lambda: ClientValueCollection(UserInfo))

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteUserGroupsData"
