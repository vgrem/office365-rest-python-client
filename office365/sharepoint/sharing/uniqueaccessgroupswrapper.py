from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sharing.uniqueaccessgroupinfo import UniqueAccessGroupInfo


@value
class UniqueAccessGroupsWrapper(ClientValue):
    discoverableByOrganization: UniqueAccessGroupInfo = field(default_factory=UniqueAccessGroupInfo)

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupsWrapper"
