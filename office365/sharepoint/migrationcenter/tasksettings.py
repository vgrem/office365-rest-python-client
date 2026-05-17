from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MigrationTaskSettings(ClientValue):
    def __init__(
        self,
        agent_group_name: Optional[str] = None,
        azure_active_directory_lkp: Optional[bool] = None,
        custom_azure_access_key: Optional[str] = None,
        custom_azure_deletion_after_mig: Optional[bool] = None,
        custom_azure_storage_account: Optional[str] = None,
        date_created: Optional[datetime] = None,
        date_modified: Optional[datetime] = None,
        delta_sync_date_time_filter: Optional[datetime] = None,
        delta_sync_enabled: Optional[bool] = None,
        enable_incremental: Optional[bool] = None,
        enable_user_mappings: Optional[bool] = None,
        encrypted: Optional[bool] = None,
        filter_out_hidden_files: Optional[bool] = None,
        filter_out_path_special_characters: Optional[bool] = None,
        ignored_file_extensions: Optional[str] = None,
        invalid_chars_replacement: Optional[str] = None,
        migrate_all_web_structures: Optional[bool] = None,
        migrate_one_note_notebook: Optional[bool] = None,
        migrate_schema: Optional[bool] = None,
        preserve_permission_for_file_share: Optional[bool] = None,
        preserve_user_permission_for_on_prem: Optional[bool] = None,
        replace_invalid_chars: Optional[bool] = None,
        scan_only: Optional[bool] = None,
        settings_update_time: Optional[datetime] = None,
        skip_list_with_audience_enabled: Optional[bool] = None,
        start_migration_automatically_when_no_scan_issue: Optional[bool] = None,
        tags: Optional[StringCollection] = None,
        turn_on_date_created_filter: Optional[bool] = None,
        turn_on_date_modified_filter: Optional[bool] = None,
        turn_on_extension_filter: Optional[bool] = None,
        use_custom_azure_storage: Optional[bool] = None,
        user_mapping_csv_file: Optional[str] = None,
        version_nums_preserved: Optional[int] = None,
    ):
        self.AgentGroupName = agent_group_name
        self.AzureActiveDirectoryLkp = azure_active_directory_lkp
        self.CustomAzureAccessKey = custom_azure_access_key
        self.CustomAzureDeletionAfterMig = custom_azure_deletion_after_mig
        self.CustomAzureStorageAccount = custom_azure_storage_account
        self.DateCreated = date_created
        self.DateModified = date_modified
        self.DeltaSyncDateTimeFilter = delta_sync_date_time_filter
        self.DeltaSyncEnabled = delta_sync_enabled
        self.EnableIncremental = enable_incremental
        self.EnableUserMappings = enable_user_mappings
        self.Encrypted = encrypted
        self.FilterOutHiddenFiles = filter_out_hidden_files
        self.FilterOutPathSpecialCharacters = filter_out_path_special_characters
        self.IgnoredFileExtensions = ignored_file_extensions
        self.InvalidCharsReplacement = invalid_chars_replacement
        self.MigrateAllWebStructures = migrate_all_web_structures
        self.MigrateOneNoteNotebook = migrate_one_note_notebook
        self.MigrateSchema = migrate_schema
        self.PreservePermissionForFileShare = preserve_permission_for_file_share
        self.PreserveUserPermissionForOnPrem = preserve_user_permission_for_on_prem
        self.ReplaceInvalidChars = replace_invalid_chars
        self.ScanOnly = scan_only
        self.SettingsUpdateTime = settings_update_time
        self.SkipListWithAudienceEnabled = skip_list_with_audience_enabled
        self.StartMigrationAutomaticallyWhenNoScanIssue = start_migration_automatically_when_no_scan_issue
        self.Tags = tags
        self.TurnOnDateCreatedFilter = turn_on_date_created_filter
        self.TurnOnDateModifiedFilter = turn_on_date_modified_filter
        self.TurnOnExtensionFilter = turn_on_extension_filter
        self.UseCustomAzureStorage = use_custom_azure_storage
        self.UserMappingCSVFile = user_mapping_csv_file
        self.VersionNumsPreserved = version_nums_preserved

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskSettings"
