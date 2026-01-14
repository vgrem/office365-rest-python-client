from office365.runtime.client_value import ClientValue


class PlacesUserEntity(ClientValue):
    def __init__(self, email: str = None, login_name: str = None, name: str = None):
        self.email = email
        self.loginName = login_name
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.PlacesUserEntity"
