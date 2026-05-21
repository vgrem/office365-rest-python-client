from dataclasses import dataclass, field
from typing import Any

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.authoringschemafeatureversion import (
    AuthoringSchemaFeatureVersion,
)


@dataclass
class SitePageCoAuthState(ClientValue):
    Action: Any = None
    HasReachedMinorVersionsLimit: Any = None
    IsNewSession: Any = None
    IsPartitionFlushed: Any = None
    LockAction: Any = None
    LockDuration: Any = None
    OverwriteExistingVersion: Any = None
    SharedLockId: Any = None
    AuthoringSchemaFeatureVersions: ClientValueCollection[AuthoringSchemaFeatureVersion] = field(
        default_factory=lambda: ClientValueCollection(AuthoringSchemaFeatureVersion)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageCoAuthState"
