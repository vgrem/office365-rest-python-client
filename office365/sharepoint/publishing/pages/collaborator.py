from typing import Optional

from office365.runtime.client_value import ClientValue


class SitePageCollaborator(ClientValue):
    def __init__(
        self, display_name: Optional[str] = None, login_name: Optional[str] = None, user_id: Optional[int] = None
    ):
        self.DisplayName = display_name
        self.LoginName = login_name
        self.UserId = user_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageCollaborator"
