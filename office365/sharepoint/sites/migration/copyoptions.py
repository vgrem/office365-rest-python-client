from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.sites.migration.moveandsharefileinfo import SPMoveAndShareFileInfo


@dataclass
class CopyMigrationOptions(ClientValue):
    AllowSchemaMismatch: bool | None = None
    AllowSmallerVersionLimitOnDestination: bool | None = None
    BypassSharedLock: bool | None = None
    ClientEtags: str | None = None
    CustomizedItemName: StringCollection = field(default_factory=StringCollection)
    ExcludeChildren: Optional[bool] = None
    IgnoreVersionHistory: Optional[bool] = None
    IncludeItemPermissions: Optional[bool] = None
    IsMoveMode: Optional[bool] = None
    MergeEmailNotifications: Optional[bool] = None
    MoveAndShareFileInfo: SPMoveAndShareFileInfo = field(default_factory=SPMoveAndShareFileInfo)
    MoveAndShareItems: Optional[bool] = None
    MoveButKeepSource: Optional[bool] = None
    NameConflictBehavior: Optional[int] = None
    SameWebCopyMoveOptimization: Optional[bool] = None
