from typing import Optional

from office365.runtime.client_value import ClientValue


class SharingLinkTemplate(ClientValue):
    def __init__(
        self,
        password_protected: Optional[bool] = None,
        role: Optional[int] = None,
        scope: Optional[int] = None,
        variant: Optional[int] = None,
    ):
        self.passwordProtected = password_protected
        self.role = role
        self.scope = scope
        self.variant = variant

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkTemplate"
