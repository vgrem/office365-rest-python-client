from office365.runtime.client_value import ClientValue


class Recipient(ClientValue):
    def __init__(self, alias: str = None, email: str = None, object_id: str = None):
        self.alias = alias
        self.email = email
        self.objectId = object_id

    @property
    def entity_type_name(self):
        return "SP.Sharing.Recipient"
