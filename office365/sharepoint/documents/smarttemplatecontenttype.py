from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SmartTemplateContentType(ClientValue):
    Id: str | None = None
    Name: str | None = None
    PublishStatus: str | None = None
