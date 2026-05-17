from office365.runtime.client_value import ClientValue
from typing import Optional


class M365TabItem(ClientValue):
    def __init__(
        self,
        display_name: Optional[str] = None,
        is_default: Optional[bool] = None,
        item_type: Optional[int] = None,
        url: Optional[str] = None,
    ):
        self.displayName = display_name
        self.isDefault = is_default
        self.itemType = item_type
        self.url = url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.M365TabItem"
