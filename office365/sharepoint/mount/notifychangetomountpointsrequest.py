from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class NotifyChangeToMountPointsRequest(ClientValue):
    MountPointUniqueIds: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.NotifyChangeToMountPointsRequest"
