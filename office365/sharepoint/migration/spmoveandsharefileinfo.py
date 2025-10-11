from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SPMoveAndShareFileInfo(ClientValue):

    def __init__(
        self,
        item_permissionable_user_ids: ClientValueCollection[int] = ClientValueCollection(int),
    ):
        self.item_permissionable_user_ids = item_permissionable_user_ids
