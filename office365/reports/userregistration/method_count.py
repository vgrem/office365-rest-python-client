from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UserRegistrationMethodCount(ClientValue):
    """Represents the number of users registered for an authentication method.

    :param str authentication_method: Name of the authentication method.
    :param str user_count: Number of users registered.
    """

    authenticationMethod: str | None = None
    userCount: int | None = None

    def __repr__(self):
        return f"{self.authenticationMethod}: {self.userCount}"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserRegistrationMethodCount"
