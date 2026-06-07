from office365.sharepoint.entity import Entity


class Authentication(Entity):
    """
    Exposes relationships that represent the authentication methods.
    """

    @property
    def entity_type_name(self) -> str:
        return "SP.OAuth.Authentication"
