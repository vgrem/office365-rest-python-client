from office365.runtime.client_value import ClientValue
from typing import Optional


class LinkTarget(ClientValue):
    def __init__(
        self,
        object_id: Optional[str] = None,
        object_sub_type: Optional[int] = None,
        object_type: Optional[int] = None,
    ):
        self.ObjectId = object_id
        self.ObjectSubType = object_sub_type
        self.ObjectType = object_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.LinkTarget"
