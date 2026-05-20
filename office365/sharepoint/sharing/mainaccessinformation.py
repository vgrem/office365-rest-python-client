from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.itemsharingsettings import ItemSharingSettings
from office365.sharepoint.sharing.mainlinkinfo import MainLinkInfo


@dataclass
class MainAccessInformation(ClientValue):
    defaultMainLinkRole: int | None = None
    mainLink: MainLinkInfo = field(default_factory=MainLinkInfo)
    sharingSettings: ItemSharingSettings = field(default_factory=ItemSharingSettings)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainAccessInformation"
