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
        canvas_element: str = None,
        code: str = None,
        endpoint: ClientAmplifyEndpointInfo = ClientAmplifyEndpointInfo(),
        event_id: str = None,
        expected: bool = None,
        extra_properties: ClientValueCollection[ClientAmplifyExtraProperty] = ClientValueCollection(
            ClientAmplifyExtraProperty
        ),
        internal_description: str = None,
        origin: str = None,
        stage: str = None,
        status_indicative: bool = None,
        step: str = None,
        timestamp_utc: str = None,
        upstream_error_code: str = None,
        upstream_http_status_code: int = None,
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
