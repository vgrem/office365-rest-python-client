from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class NotifyChangeToMountPointsRequest(ClientValue):

    def __init__(self, mount_point_unique_ids: GuidCollection = GuidCollection()):
        self.MountPointUniqueIds = mount_point_unique_ids

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.NotifyChangeToMountPointsRequest"
