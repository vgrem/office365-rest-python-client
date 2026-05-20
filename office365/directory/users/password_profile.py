from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PasswordProfile(ClientValue):
    """
        Contains the password profile associated with a user. The passwordProfile property of the user entity is a
    passwordProfile object.
        Fields:
            password (str): The password for the user. This property is required when a user is created.
            force_change_password_next_sign_in (bool): true if the user must change her password on the next login;
            force_change_password_next_sign_in_with_mfa (bool): f true, at next sign-in, the user must perform a
    """

    password: str | None = None
    forceChangePasswordNextSignIn: bool | None = None
    forceChangePasswordNextSignInWithMfa: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.PasswordProfile"
