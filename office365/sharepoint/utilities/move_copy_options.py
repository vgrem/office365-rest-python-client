from __future__ import annotations

from typing import Optional

from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class MoveCopyOptions(ClientValue):

    KeepBoth: bool = True
    ResetAuthorAndCreatedOnCopy: bool = False
    RetainEditorAndModifiedOnMove: bool = False
    ShouldBypassSharedLocks: bool = False

    @property
    def entity_type_name(self):
        return "SP.MoveCopyOptions"