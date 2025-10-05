from office365.runtime.client_value import ClientValue


class IBSegmentInfo(ClientValue):

    def __init__(self, display_name: str = None, object_id: str = None):
        self.DisplayName = display_name
        self.ObjectId = object_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.IBSegmentInfo"
