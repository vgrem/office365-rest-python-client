from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SmartTemplateContentType(ClientValue):
    Id: str | None = None
    Name: str | None = None
    PublishStatus: str | None = None
