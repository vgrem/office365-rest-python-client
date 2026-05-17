from office365.runtime.client_value import ClientValue
from typing import Optional


class UpdateCardElement(ClientValue):
    def __init__(self, is_visible: Optional[bool] = None, type_: Optional[str] = None, value: Optional[str] = None):
        self.isVisible = is_visible
        self.type = type_
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCardElement"
