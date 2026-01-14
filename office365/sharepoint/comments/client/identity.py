from office365.runtime.client_value import ClientValue


class Identity(ClientValue):
    def __init__(
        self,
        email: str = None,
        id_: int = None,
        login_name: str = None,
        name: str = None,
    ):
        self.email = email
        self.id = id_
        self.loginName = login_name
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.Client.Identity"
