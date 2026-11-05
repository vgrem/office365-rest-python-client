from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class UserInformation(ClientValue):
    Id: Optional[str] = None
    Name: Optional[str] = None
    Puid: Optional[str] = None

    @property
    def entity_type_name(self):
        return "MS.FileServices.UserInformation"
