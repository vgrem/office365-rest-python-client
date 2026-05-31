from datetime import datetime
from typing import Optional

from office365.directory.authentication.methods.method import AuthenticationMethod
from office365.runtime.types.odata_property import odata


class PasswordAuthenticationMethod(AuthenticationMethod):
    """A representation of a user's password. For security, the password itself will never be returned in the object,
    but action can be taken to reset a password."""

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """The date and time when this password was last updated. This property is currently not populated."""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def password(self) -> Optional[str]:
        """For security, the password is always returned as null from a LIST or GET operation."""
        return self.properties.get("password", None)
