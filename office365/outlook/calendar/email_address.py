from typing import Optional

from office365.runtime.client_value import ClientValue


class EmailAddress(ClientValue):
    """The name and email address of a contact or message recipient."""

    def __init__(self, address: Optional[str] = None, name: Optional[str] = None):
        """
        :param str address: The email address of the person or entity.
        :param str name: The display name of the person or entity.
        """
        super().__init__()
        self.address = address
        self.name = name

    def __str__(self):
        return self.address or ""

    def __repr__(self):
        return f"{self.name or ''} <{self.address or ''}>"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EmailAddress"
