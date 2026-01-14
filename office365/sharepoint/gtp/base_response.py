from office365.runtime.client_value import ClientValue


class BaseGptResponse(ClientValue):
    def __init__(
        self,
        created: int = None,
        id_: str = None,
        model: str = None,
        object_type: str = None,
    ):
        self.Created = created
        self.Id = id_
        self.Model = model
        self.ObjectType = object_type

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.BaseGptResponse"
