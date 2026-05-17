from typing import Optional

from office365.runtime.client_value import ClientValue


class ClientAmplifyExtraProperty(ClientValue):
    def __init__(self, name: Optional[str] = None, value: Optional[str] = None):
        self.name = name
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyExtraProperty"
