from office365.runtime.client_value import ClientValue


class ActivityClientIdentity(ClientValue):
    def __init__(self, email: str = None, name: str = None, id_: str = None, provider: str = None):
        self.email = email
        self.name = name
        self.id = id_
        self.provider = provider

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientIdentity"
