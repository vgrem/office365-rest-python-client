from typing import Optional

from office365.directory.authentication.methods.method import AuthenticationMethod
from office365.runtime.types.odata_property import odata


class EmailAuthenticationMethod(AuthenticationMethod):
    """
    Represents an email address registered to a user. Email as an authentication method is available only for
    self-service password reset (SSPR). Users may only have one email authentication method.
    """

    @odata(name="emailAddress")
    @property
    def email_address(self) -> Optional[str]:
        """The email address registered to this user."""
        return self.properties.get("emailAddress", None)
