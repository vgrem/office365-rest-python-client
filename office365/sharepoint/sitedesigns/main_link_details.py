from __future__ import annotations

from office365.runtime.client_value import ClientValue


class MainLinkDetails(ClientValue):
    Audience: int | None = None
    Role: int | None = None
