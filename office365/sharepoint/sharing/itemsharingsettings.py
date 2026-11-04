from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ItemSharingSettings(ClientValue):
    blockSharingPushDown: bool | None = None
    itemId: str | None = None
    itemMembersCanShare: bool | None = None
    itemName: str | None = None
    itemType: int | None = None
    parentId: str | None = None
    blockMembersCanShare: bool | None = None
    blockSharingPushdown: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.ItemSharingSettings"
