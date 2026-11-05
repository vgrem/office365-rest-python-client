from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FileDeleteParameters(ClientValue):
    BypassCheckedOut: bool | None = None
    BypassSharedLock: bool | None = None
    ETagMatch: str | None = None
