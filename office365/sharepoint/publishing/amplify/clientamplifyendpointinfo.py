from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.clientamplifyextraproperty import (
    ClientAmplifyExtraProperty,
)


class ClientAmplifyEndpointInfo(ClientValue):

    def __init__(
        self,
        endpoint_sub_type: str = None,
        endpoint_type: str = None,
        extra_properties: ClientValueCollection[ClientAmplifyExtraProperty] = ClientValueCollection(
            ClientAmplifyExtraProperty
        ),
        href: str = None,
        id_: str = None,
        name: str = None,
    ):
        self.endpointSubType = endpoint_sub_type
        self.endpointType = endpoint_type
        self.extraProperties = extra_properties
        self.href = href
        self.id = id_
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyEndpointInfo"
