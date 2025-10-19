from office365.runtime.client_value import ClientValue


class UserCreationInformation(ClientValue):

    def __init__(self, email: str = None, login_name: str = None, title: str = None):
        self.email = email
        self.login_name = login_name
        self.title = title
