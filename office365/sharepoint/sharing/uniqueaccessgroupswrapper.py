from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.uniqueaccessgroupinfo import UniqueAccessGroupInfo


@dataclass
class UniqueAccessGroupsWrapper(ClientValue):
    discoverableByOrganization: UniqueAccessGroupInfo = field(default_factory=UniqueAccessGroupInfo)

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupsWrapper"
