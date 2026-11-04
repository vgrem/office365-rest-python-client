from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sharing.itemsharingsettings import ItemSharingSettings
from office365.sharepoint.sharing.mainlinkinfo import MainLinkInfo


@value
class MainAccessInformation(ClientValue):
    defaultMainLinkRole: int | None = None
    mainLink: MainLinkInfo = field(default_factory=MainLinkInfo)
    sharingSettings: ItemSharingSettings = field(default_factory=ItemSharingSettings)

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainAccessInformation"
