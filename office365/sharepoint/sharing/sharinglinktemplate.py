from office365.runtime.client_value import ClientValue


class SharingLinkTemplate(ClientValue):

    def __init__(
        self,
        password_protected: bool = None,
        role: int = None,
        scope: int = None,
        variant: int = None,
    ):
        self.passwordProtected = password_protected
        self.role = role
        self.scope = scope
        self.variant = variant

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkTemplate"
