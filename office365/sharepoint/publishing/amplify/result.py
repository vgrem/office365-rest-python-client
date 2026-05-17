from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.clientamplifyendpointinfo import (
    ClientAmplifyEndpointInfo,
)
from office365.sharepoint.publishing.amplify.clientamplifyextraproperty import (
    ClientAmplifyExtraProperty,
)


class ClientAmplifyResult(ClientValue):
    def __init__(
        self,
        canvas_element: Optional[str] = None,
        code: Optional[str] = None,
        endpoint: ClientAmplifyEndpointInfo = ClientAmplifyEndpointInfo(),
        event_id: Optional[str] = None,
        expected: Optional[bool] = None,
        extra_properties: ClientValueCollection[ClientAmplifyExtraProperty] = ClientValueCollection(
            ClientAmplifyExtraProperty
        ),
        internal_description: Optional[str] = None,
        origin: Optional[str] = None,
        stage: Optional[str] = None,
        status_indicative: Optional[bool] = None,
        step: Optional[str] = None,
        timestamp_utc: Optional[str] = None,
        upstream_error_code: Optional[str] = None,
        upstream_http_status_code: Optional[int] = None,
    ):
        self.canvasElement = canvas_element
        self.code = code
        self.endpoint = endpoint
        self.eventId = event_id
        self.expected = expected
        self.extraProperties = extra_properties
        self.internalDescription = internal_description
        self.origin = origin
        self.stage = stage
        self.statusIndicative = status_indicative
        self.step = step
        self.timestampUTC = timestamp_utc
        self.upstreamErrorCode = upstream_error_code
        self.upstreamHttpStatusCode = upstream_http_status_code

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Amplify.Client.ClientAmplifyResult"
