from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.migration.spmoveandsharefileinfo import SPMoveAndShareFileInfo


class CopyMigrationOptions(ClientValue):
    """ """

    def __init__(
        self,
        allow_schema_mismatch=None,
        allow_smaller_version_limit_on_destination=None,
        bypass_shared_lock=None,
        client_etags=None,
        customized_item_name: StringCollection = StringCollection(),
        exclude_children: bool = None,
        ignore_version_history: bool = None,
        include_item_permissions: bool = None,
        is_move_mode: bool = None,
        merge_email_notifications: bool = None,
        move_and_share_file_info: SPMoveAndShareFileInfo = SPMoveAndShareFileInfo(),
        move_and_share_items: bool = None,
        move_but_keep_source: bool = None,
        name_conflict_behavior: int = None,
        same_web_copy_move_optimization: bool = None,
    ):
        self.AllowSchemaMismatch = allow_schema_mismatch
        self.AllowSmallerVersionLimitOnDestination = allow_smaller_version_limit_on_destination
        self.BypassSharedLock = bypass_shared_lock
        self.ClientEtags = client_etags
        self.CustomizedItemName = customized_item_name
        self.ExcludeChildren = exclude_children
        self.IgnoreVersionHistory = ignore_version_history
        self.IncludeItemPermissions = include_item_permissions
        self.IsMoveMode = is_move_mode
        self.MergeEmailNotifications = merge_email_notifications
        self.MoveAndShareFileInfo = move_and_share_file_info
        self.MoveAndShareItems = move_and_share_items
        self.MoveButKeepSource = move_but_keep_source
        self.NameConflictBehavior = name_conflict_behavior
        self.SameWebCopyMoveOptimization = same_web_copy_move_optimization
