from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.creatable_item_info import CreatableItemInfo


class CreatableItemInfoCollection(ClientValue):
    """Represents a collection of CreatableItemInfo (section 3.2.5.283) objects."""

    def __init__(self, items=None):
        """
        :param list[CreatableItemInfo] items:
        """
        super().__init__()
        self.Items = ClientValueCollection(CreatableItemInfo, items)
