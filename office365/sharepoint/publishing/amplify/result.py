from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.clientamplifyendpointinfo import (
    ClientAmplifyEndpointInfo,
)
from office365.sharepoint.publishing.amplify.clientamplifyextraproperty import (
    ClientAmplifyExtraProperty,
)


@dataclass
class ClientAmplifyResult(ClientValue):
    canvasElement: Optional[str] = None
    code: Optional[str] = None
    endpoint: ClientAmplifyEndpointInfo = field(default_factory=lambda: ClientAmplifyEndpointInfo())
    eventId: Optional[str] = None
    expected: Optional[bool] = None
    extraProperties: ClientValueCollection[ClientAmplifyExtraProperty] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyExtraProperty)
    )
    internalDescription: Optional[str] = None
    origin: Optional[str] = None
    stage: Optional[str] = None
    statusIndicative: Optional[bool] = None
    step: Optional[str] = None
    timestampUTC: Optional[str] = None
    upstreamErrorCode: Optional[str] = None
    upstreamHttpStatusCode: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyResult"
