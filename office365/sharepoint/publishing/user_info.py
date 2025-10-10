from office365.runtime.client_value import ClientValue


class UserInfo(ClientValue):

    def __init__(
        self,
        email: str = None,
        login_name: str = None,
        name: str = None,
        user_principal_name: str = None,
    ):
        self.email = email
        self.loginName = login_name
        self.name = name
        self.userPrincipalName = user_principal_name

    "Represents user information of a user with consistent color and acronym for client rendering."

    @property
    def entity_type_name(self):
        return "SP.Publishing.UserInfo"
