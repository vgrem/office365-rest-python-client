from office365.runtime.client_value import ClientValue


class SitePageCollaborator(ClientValue):

    def __init__(self, display_name: str = None, login_name: str = None, user_id: int = None):
        self.DisplayName = display_name
        self.LoginName = login_name
        self.UserId = user_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageCollaborator"
