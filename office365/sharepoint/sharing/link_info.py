from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.inherited_from import InheritedFrom
from office365.sharepoint.sharing.links.info import SharingLinkInfo
from office365.sharepoint.sharing.principal import Principal


@dataclass
class LinkInfo(ClientValue):
    """This class provides metadata for the tokenized sharing link including settings details, inheritance status,
    and an optional array of members.

    Args:
        is_inherited (bool): Boolean that indicates if the tokenized sharing link is present due to inherited
            permissions from a parent object.
    """

    inherited_from: InheritedFrom = field(default_factory=InheritedFrom)
    isInherited: bool | None = None
    linkDetails: SharingLinkInfo = field(default_factory=SharingLinkInfo)
    linkMembers: ClientValueCollection[Principal] = field(default_factory=lambda: ClientValueCollection(Principal))
    linkStatus: int | None = None
    totalLinkMembersCount: int | None = None
    inheritedFrom: InheritedFrom = field(default_factory=InheritedFrom)

    @property
    def entity_type_name(self):
        return "SP.Sharing.LinkInfo"
