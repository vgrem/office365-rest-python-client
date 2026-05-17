from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


class MainLinkInfo(ClientValue):
    def __init__(
        self,
        accessors: ClientValueCollection[Principal] = ClientValueCollection(Principal),
        audience: Optional[int] = None,
        role: Optional[int] = None,
        share_id: Optional[UUID] = None,
        url: Optional[str] = None,
    ):
        self.accessors = accessors
        self.audience = audience
        self.role = role
        self.shareId = share_id
        self.url = url

    @property
    def entity_type_name(self):
        return "SP.Sharing.MainLinkInfo"
