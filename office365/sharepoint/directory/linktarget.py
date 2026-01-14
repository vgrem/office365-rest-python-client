from office365.runtime.client_value import ClientValue


class LinkTarget(ClientValue):
    def __init__(
        self,
        object_id: str = None,
        object_sub_type: int = None,
        object_type: int = None,
    ):
        self.ObjectId = object_id
        self.ObjectSubType = object_sub_type
        self.ObjectType = object_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.LinkTarget"
