from __future__ import annotations


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class MoveCopyOptions(ClientValue):

    KeepBoth = True
    ResetAuthorAndCreatedOnCopy = False
    RetainEditorAndModifiedOnMove = False
    ShouldBypassSharedLocks = False

    @property
    def entity_type_name(self):
        return "SP.MoveCopyOptions"