from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SitePageCollaborator(ClientValue):
    DisplayName: Optional[str] = None
    LoginName: Optional[str] = None
    UserId: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageCollaborator"
