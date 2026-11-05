from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.uniqueaccessgroupinfo import UniqueAccessGroupInfo


class UniqueAccessGroupsWrapper(ClientValue):
    discoverableByOrganization: UniqueAccessGroupInfo = field(default_factory=UniqueAccessGroupInfo)

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupsWrapper"
