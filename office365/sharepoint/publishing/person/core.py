from typing import Optional

from office365.runtime.client_value import ClientValue


class PersonCore(ClientValue):
    def __init__(
        self, aad_object_id: Optional[str] = None, display_name: Optional[str] = None, user_name: Optional[str] = None
    ):
        self.AadObjectId = aad_object_id
        self.DisplayName = display_name
        self.UserName = user_name

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonCore"
