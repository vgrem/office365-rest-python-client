from typing import Optional

from office365.runtime.client_value import ClientValue


class OfficeFileUserValueResponse(ClientValue):
    def __init__(self, key: Optional[str] = None, value: Optional[str] = None):
        self.key = key
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.UserActions.OfficeFileUserValueResponse"
