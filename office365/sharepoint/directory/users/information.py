from typing import Optional

from office365.runtime.client_value import ClientValue


class UserInformation(ClientValue):
    def __init__(self, id_: Optional[str] = None, name: Optional[str] = None, puid: Optional[str] = None):
        self.Id = id_
        self.Name = name
        self.Puid = puid

    @property
    def entity_type_name(self):
        return "MS.FileServices.UserInformation"
