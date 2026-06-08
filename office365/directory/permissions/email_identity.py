from typing import Optional

from office365.directory.permissions.identity import Identity


class EmailIdentity(Identity):
    """Represents the email identity of a user."""

    def __init__(self, id_: Optional[str] = None, email: Optional[str] = None, display_name: Optional[str] = None):
        """Args:
        email (str):
        """
        super().__init__(display_name, id_)
        self.email = email
