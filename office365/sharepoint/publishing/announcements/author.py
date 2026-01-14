from office365.runtime.client_value import ClientValue


class AnnouncementAuthor(ClientValue):
    def __init__(self, email: str = None, id_: str = None, name: str = None):
        self.Email = email
        self.ID = id_
        self.Name = name

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementAuthor"
