from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


@dataclass
class OversharedWebInfo(ClientValue):
    hasUniqueRoleAssignmentsForList: bool | None = None
    principals: ClientValueCollection[Principal] = field(default_factory=lambda: ClientValueCollection(Principal))

    @property
    def entity_type_name(self):
        return "SP.Sharing.OversharedWebInfo"
