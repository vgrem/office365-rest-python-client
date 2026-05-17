from office365.runtime.client_value import ClientValue
from typing import Optional


class IBSegmentInfo(ClientValue):
    def __init__(self, display_name: Optional[str] = None, object_id: Optional[str] = None):
        self.DisplayName = display_name
        self.ObjectId = object_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Portal.IBSegmentInfo"
