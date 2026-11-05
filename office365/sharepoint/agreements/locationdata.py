from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AgreementLocationData(ClientValue):
    LibraryId: str | None = None
    SiteId: str | None = None
    WebId: str | None = None
