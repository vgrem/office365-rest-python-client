from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MigrationTaskSettings(ClientValue):
    def __init__(
        self,
        agent_group_name: str = None,
        azure_active_directory_lkp: bool = None,
        custom_azure_access_key: str = None,
        custom_azure_deletion_after_mig: bool = None,
        custom_azure_storage_account: str = None,
        date_created: datetime = None,
        date_modified: datetime = None,
        delta_sync_date_time_filter: datetime = None,
        delta_sync_enabled: bool = None,
        enable_incremental: bool = None,
        enable_user_mappings: bool = None,
        encrypted: bool = None,
        filter_out_hidden_files: bool = None,
        filter_out_path_special_characters: bool = None,
        ignored_file_extensions: str = None,
        invalid_chars_replacement: str = None,
        migrate_all_web_structures: bool = None,
        migrate_one_note_notebook: bool = None,
        migrate_schema: bool = None,
        preserve_permission_for_file_share: bool = None,
        preserve_user_permission_for_on_prem: bool = None,
        replace_invalid_chars: bool = None,
        scan_only: bool = None,
        settings_update_time: datetime = None,
        skip_list_with_audience_enabled: bool = None,
        start_migration_automatically_when_no_scan_issue: bool = None,
        tags: StringCollection = None,
        turn_on_date_created_filter: bool = None,
        turn_on_date_modified_filter: bool = None,
        turn_on_extension_filter: bool = None,
        use_custom_azure_storage: bool = None,
        user_mapping_csv_file: str = None,
        version_nums_preserved: int = None,
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
