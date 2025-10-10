from office365.runtime.client_value import ClientValue


class EmailData(ClientValue):

    def __init__(self, body: str = None, subject: str = None):
        self.body = body
        self.subject = subject

    @property
    def entity_type_name(self):
        return "SP.Sharing.EmailData"
