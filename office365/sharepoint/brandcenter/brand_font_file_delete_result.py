from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BrandFontFileDeleteResult(ClientValue):
    GeoLocation: str | None = None
    Message: str | None = None
    Status: str | None = None
