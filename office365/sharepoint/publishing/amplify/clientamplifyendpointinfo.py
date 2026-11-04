from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.publishing.amplify.clientamplifyextraproperty import (
    ClientAmplifyExtraProperty,
)


@value
class ClientAmplifyEndpointInfo(ClientValue):
    endpointSubType: Optional[str] = None
    endpointType: Optional[str] = None
    extraProperties: ClientValueCollection[ClientAmplifyExtraProperty] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyExtraProperty)
    )
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyEndpointInfo"
