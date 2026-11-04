from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserCreationInformation(ClientValue):
    Email: str | None = None
    LoginName: str | None = None
    Title: str | None = None
