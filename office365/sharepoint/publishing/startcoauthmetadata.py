from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.authoringschemafeatureversion import (
    AuthoringSchemaFeatureVersion,
)


@dataclass
class StartCoAuthMetaData(ClientValue):
    AuthoringSchemaFeatureVersions: ClientValueCollection[AuthoringSchemaFeatureVersion] = field(
        default_factory=lambda: ClientValueCollection(AuthoringSchemaFeatureVersion)
    )
    ForceCheckin: Optional[bool] = None
    ForceFlushOpStream: Optional[bool] = None
    IsUserConsentProvidedForModerationStatus: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.StartCoAuthMetaData"
