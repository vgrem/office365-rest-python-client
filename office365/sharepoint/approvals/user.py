from office365.runtime.client_value import ClientValue


class UserDTO(ClientValue):

    def __init__(self, email: str = None, login_name: str = None):
        self.Email = email
        self.LoginName = login_name
