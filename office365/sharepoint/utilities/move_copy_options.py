from __future__ import annotations

from office365.runtime.client_value import ClientValue


class MoveCopyOptions(ClientValue):
    KeepBoth: bool = True
    ResetAuthorAndCreatedOnCopy: bool = False
    RetainEditorAndModifiedOnMove: bool = False
    ShouldBypassSharedLocks: bool = False

    @property
    def entity_type_name(self):
        return "SP.MoveCopyOptions"
