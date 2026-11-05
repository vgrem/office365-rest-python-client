from typing import Optional

from office365.runtime.client_value import ClientValue


class ClientAmplifyExtraProperty(ClientValue):
    name: Optional[str] = None
    value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyExtraProperty"
