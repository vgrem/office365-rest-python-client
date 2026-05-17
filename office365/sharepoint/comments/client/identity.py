from typing import Optional

from office365.runtime.client_value import ClientValue


class Identity(ClientValue):
    def __init__(
        self,
        email: Optional[str] = None,
        id_: Optional[int] = None,
        login_name: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.email = email
        self.id = id_
        self.loginName = login_name
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.Client.Identity"
