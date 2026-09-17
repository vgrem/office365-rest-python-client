"""Built-in SharePoint field internal names — the single source of truth.

The names come from the MS-WSSTS "Data Fields" specification
(https://learn.microsoft.com/en-us/openspecs/sharepoint_protocols/ms-wssts/83747ceb-f9a5-456b-bc45-692671c6ce6b).
Use :data:`SYSTEM_FIELD_NAMES` to filter system/bookkeeping columns out of a
projection or schema (migration, assessment, exporters).
"""

from __future__ import annotations


class SPBuiltInFieldName:
    """Internal names of the built-in (system) SharePoint fields (MS-WSSTS)."""

    _CopySource = "_CopySource"
    _HasCopyDestinations = "_HasCopyDestinations"
    _IsCurrentVersion = "_IsCurrentVersion"
    _Level = "_Level"
    _ModerationStatus = "_ModerationStatus"
    _UIVersion = "_UIVersion"
    _UIVersionString = "_UIVersionString"
    Author = "Author"
    BaseName = "BaseName"
    ContentType = "ContentType"
    ContentTypeId = "ContentTypeId"
    Created = "Created"
    Created_x0020_Date = "Created_x0020_Date"
    Editor = "Editor"
    EncodedAbsUrl = "EncodedAbsUrl"
    File_x0020_Type = "File_x0020_Type"
    FileDirRef = "FileDirRef"
    FileLeafRef = "FileLeafRef"
    FileRef = "FileRef"
    FolderChildCount = "FolderChildCount"
    FSObjType = "FSObjType"
    ID = "ID"
    InstanceID = "InstanceID"
    ItemChildCount = "ItemChildCount"
    Last_x0020_Modified = "Last_x0020_Modified"
    MetaInfo = "MetaInfo"
    Modified = "Modified"
    Order = "Order"
    owshiddenversion = "owshiddenversion"
    PermMask = "PermMask"
    ProgId = "ProgId"
    ScopeId = "ScopeId"
    ServerUrl = "ServerUrl"
    SortBehavior = "SortBehavior"
    SyncClientId = "SyncClientId"
    UniqueId = "UniqueId"

    ALL: frozenset[str] = frozenset(
        {
            _CopySource,
            _HasCopyDestinations,
            _IsCurrentVersion,
            _Level,
            _ModerationStatus,
            _UIVersion,
            _UIVersionString,
            Author,
            BaseName,
            ContentType,
            ContentTypeId,
            Created,
            Created_x0020_Date,
            Editor,
            EncodedAbsUrl,
            File_x0020_Type,
            FileDirRef,
            FileLeafRef,
            FileRef,
            FolderChildCount,
            FSObjType,
            ID,
            InstanceID,
            ItemChildCount,
            Last_x0020_Modified,
            MetaInfo,
            Modified,
            Order,
            owshiddenversion,
            PermMask,
            ProgId,
            ScopeId,
            ServerUrl,
            SortBehavior,
            SyncClientId,
            UniqueId,
        }
    )

    @classmethod
    def is_builtin(cls, name: str) -> bool:
        """Whether ``name`` is a built-in SharePoint field internal name."""
        return name in cls.ALL


# System/bookkeeping columns that SharePoint exposes but the MS-WSSTS "Data
# Fields" list does not enumerate (moderation, versioning, app metadata, ...).
EXTRA_SYSTEM_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "AppAuthor",
        "AppEditor",
        "Attachments",
        "ComplianceAssetId",
        "EffectivePermMask",
        "GUID",
        "Version",
        "VirusStatus",
        "WorkflowVersion",
        "_CheckinComment",
        "_ColorHex",
        "_ColorTag",
        "_CopySource",
        "_Emoji",
        "_HasCopyDestinations",
        "_ModerationComments",
    }
)

#: Every known system column internal name (spec + library extras).
SYSTEM_FIELD_NAMES: frozenset[str] = SPBuiltInFieldName.ALL | EXTRA_SYSTEM_FIELD_NAMES
