from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class FolderDeleteParameters(ClientValue):
    BypassSharedLock: bool | None = None
    DeleteIfEmpty: bool | None = None
    BypassCheckedOut: bool | None = None
    ETagMatch: str | None = None
