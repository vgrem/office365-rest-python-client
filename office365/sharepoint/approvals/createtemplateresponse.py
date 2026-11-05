from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class CreateTemplateResponse(ClientValue):
    ServerRelativeUrl: Optional[str] = None
    Title: Optional[str] = None
    UniqueID: Optional[str] = None
    Url: Optional[str] = None
