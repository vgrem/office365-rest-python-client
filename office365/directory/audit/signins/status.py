from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SignInStatus(ClientValue):
    """Provides the sign-in status (Success or Failure) of the sign-in."""

    additionalDetails: str | None = None
    errorCode: int | None = None
    failureReason: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.SignInStatus"
