from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.requestendpoint import (
    AmplifyRequestEndpoint,
)


class AmplifyRequestParams(ClientValue):

    def __init__(
        self,
        endpoints: ClientValueCollection[
            AmplifyRequestEndpoint
        ] = ClientValueCollection(AmplifyRequestEndpoint),
        use_new_publishing_stack: bool = None,
    ):
        self.Endpoints = endpoints
        self.UseNewPublishingStack = use_new_publishing_stack
