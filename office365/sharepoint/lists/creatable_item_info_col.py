from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.creatable_item_info import CreatableItemInfo


class CreatableItemInfoCollection(ClientValue):
    """Represents a collection of CreatableItemInfo (section 3.2.5.283) objects."""

    Items: ClientValueCollection[CreatableItemInfo] = field(
        default_factory=lambda: ClientValueCollection(CreatableItemInfo)
    )
