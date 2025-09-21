from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.shared_with_user import SharedWithUser


class SharedWithUserCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[SharedWithUser] = ClientValueCollection(
            SharedWithUser
        ),
    ):
        self.items = items
