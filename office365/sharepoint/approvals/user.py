from typing import Optional

from office365.runtime.client_value import ClientValue


class UserDTO(ClientValue):
    def __init__(self, email: Optional[str] = None, login_name: Optional[str] = None):
        self.Email = email
        self.LoginName = login_name
