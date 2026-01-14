from office365.runtime.client_value import ClientValue


class UpdateCardElement(ClientValue):
    def __init__(self, is_visible: bool = None, type_: str = None, value: str = None):
        self.isVisible = is_visible
        self.type = type_
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCardElement"
