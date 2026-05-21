from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.requestendpoint import (
    AmplifyRequestEndpoint,
)


@dataclass
class AmplifyRequestParams(ClientValue):
    Endpoints: ClientValueCollection[AmplifyRequestEndpoint] = field(
        default_factory=lambda: ClientValueCollection(AmplifyRequestEndpoint)
    )
    UseNewPublishingStack: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyRequestParams"
