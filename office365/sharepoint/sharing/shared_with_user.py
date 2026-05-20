from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharedWithUser(ClientValue):
    """
    Returns the array of users that have been shared in sharing action for the change log.

    Fields:
        Email: Gets the email of the principal.
        Name: Gets the name of the principal.
    """

    Email: str | None = None
    Name: str | None = None
