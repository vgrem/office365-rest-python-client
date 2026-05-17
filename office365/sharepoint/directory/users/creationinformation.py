from typing import Optional

from office365.runtime.client_value import ClientValue


class UserCreationInformation(ClientValue):
    def __init__(self, email: Optional[str] = None, login_name: Optional[str] = None, title: Optional[str] = None):
        self.email = email
        self.login_name = login_name
        self.title = title
