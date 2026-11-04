from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AppViewCreationInfo(ClientValue):
    AppId: UUID | None = None
    IsPrivate: bool | None = None
    Title: str | None = None
