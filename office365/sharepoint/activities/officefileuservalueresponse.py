from office365.runtime.client_value import ClientValue


class OfficeFileUserValueResponse(ClientValue):

    def __init__(self, key: str = None, value: str = None):
        self.key = key
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.UserActions.OfficeFileUserValueResponse"
