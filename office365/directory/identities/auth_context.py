from __future__ import annotations

from office365.directory.identities.sign_in_context import SignInContext


class AuthContext(SignInContext):
    authenticationContextValue: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthContext"
