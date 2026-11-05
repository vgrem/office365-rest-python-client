from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FolderDeleteParameters(ClientValue):
    BypassSharedLock: bool | None = None
    DeleteIfEmpty: bool | None = None
    BypassCheckedOut: bool | None = None
    ETagMatch: str | None = None
