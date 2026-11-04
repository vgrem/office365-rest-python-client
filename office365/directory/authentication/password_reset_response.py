from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PasswordResetResponse(ClientValue):
    """Represents the new system-generated password after a password reset operation.

    Args:
        new_password (str): The Azure AD-generated password.
    """

    newPassword: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PasswordResetResponse"
