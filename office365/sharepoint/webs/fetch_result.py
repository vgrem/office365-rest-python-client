from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WebFetchResult(ClientValue):
    Content: str | None = None
    ContentLength: int | None = None
    ContentType: str | None = None
    FinalUrl: str | None = None
    RequestedUrl: str | None = None
    StatusCode: int | None = None
    Truncated: bool | None = None
