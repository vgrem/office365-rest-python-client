from office365.runtime.client_value import ClientValue
from office365.sharepoint.clientsidecomponent.updatecardelement import UpdateCardElement
from typing import Optional


class ElementUpdate(ClientValue):
    def __init__(
        self,
        action: Optional[str] = None,
        element: UpdateCardElement = UpdateCardElement(),
        element_id: Optional[str] = None,
    ):
        self.action = action
        self.element = element
        self.elementId = element_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.ElementUpdate"
