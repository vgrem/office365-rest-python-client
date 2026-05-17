from office365.runtime.client_value import ClientValue
from typing import Optional


class BaseGptResponse(ClientValue):
    def __init__(
        self,
        created: Optional[int] = None,
        id_: Optional[str] = None,
        model: Optional[str] = None,
        object_type: Optional[str] = None,
    ):
        self.Created = created
        self.Id = id_
        self.Model = model
        self.ObjectType = object_type

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.BaseGptResponse"
