from office365.runtime.client_value import ClientValue
from office365.sharepoint.actionablemessages.updatecardelement import UpdateCardElement


class ElementUpdate(ClientValue):

    def __init__(
        self,
        action: str = None,
        element: UpdateCardElement = UpdateCardElement(),
        element_id: str = None,
    ):
        self.action = action
        self.element = element
        self.elementId = element_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.ElementUpdate"
