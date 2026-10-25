from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MigrationTaskEntityData(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskEntityData"

    @odata(name="AgentGroupName")
    @property
    def agent_group_name(self) -> Optional[str]:
        """Gets the AgentGroupName property"""
        return self.properties.get("AgentGroupName", None)

    @odata(name="AzureActiveDirectoryLkp")
    @property
    def azure_active_directory_lkp(self) -> Optional[bool]:
        """Gets the AzureActiveDirectoryLkp property"""
        return self.properties.get("AzureActiveDirectoryLkp", None)

    @odata(name="CustomAzureAccessKey")
    @property
    def custom_azure_access_key(self) -> Optional[str]:
        """Gets the CustomAzureAccessKey property"""
        return self.properties.get("CustomAzureAccessKey", None)

    @odata(name="CustomAzureDeletionAfterMig")
    @property
    def custom_azure_deletion_after_mig(self) -> Optional[bool]:
        """Gets the CustomAzureDeletionAfterMig property"""
        return self.properties.get("CustomAzureDeletionAfterMig", None)

    @odata(name="CustomAzureStorageAccount")
    @property
    def custom_azure_storage_account(self) -> Optional[str]:
        """Gets the CustomAzureStorageAccount property"""
        return self.properties.get("CustomAzureStorageAccount", None)

    @odata(name="DateCreated")
    @property
    def date_created(self) -> Optional[datetime]:
        """Gets the DateCreated property"""
        return self.properties.get("DateCreated", datetime.min)

    @odata(name="DateModified")
    @property
    def date_modified(self) -> Optional[datetime]:
        """Gets the DateModified property"""
        return self.properties.get("DateModified", datetime.min)

    @odata(name="DeltaSyncDateTimeFilter")
    @property
    def delta_sync_datetime_filter(self) -> Optional[datetime]:
        """Gets the DeltaSyncDateTimeFilter property"""
        return self.properties.get("DeltaSyncDateTimeFilter", datetime.min)

    @odata(name="DeltaSyncEnabled")
    @property
    def delta_sync_enabled(self) -> Optional[bool]:
        """Gets the DeltaSyncEnabled property"""
        return self.properties.get("DeltaSyncEnabled", None)

    @odata(name="EnableIncremental")
    @property
    def enable_incremental(self) -> Optional[bool]:
        """Gets the EnableIncremental property"""
        return self.properties.get("EnableIncremental", None)

    @odata(name="EnableUserMappings")
    @property
    def enable_user_mappings(self) -> Optional[bool]:
        """Gets the EnableUserMappings property"""
        return self.properties.get("EnableUserMappings", None)

    @odata(name="Encrypted")
    @property
    def encrypted(self) -> Optional[bool]:
        """Gets the Encrypted property"""
        return self.properties.get("Encrypted", None)

    @odata(name="FilterOutHiddenFiles")
    @property
    def filter_out_hidden_files(self) -> Optional[bool]:
        """Gets the FilterOutHiddenFiles property"""
        return self.properties.get("FilterOutHiddenFiles", None)

    @odata(name="FilterOutPathSpecialCharacters")
    @property
    def filter_out_path_special_characters(self) -> Optional[bool]:
        """Gets the FilterOutPathSpecialCharacters property"""
        return self.properties.get("FilterOutPathSpecialCharacters", None)

    @odata(name="IgnoredFileExtensions")
    @property
    def ignored_file_extensions(self) -> Optional[str]:
        """Gets the IgnoredFileExtensions property"""
        return self.properties.get("IgnoredFileExtensions", None)

    @odata(name="InvalidCharsReplacement")
    @property
    def invalid_chars_replacement(self) -> Optional[str]:
        """Gets the InvalidCharsReplacement property"""
        return self.properties.get("InvalidCharsReplacement", None)

    @odata(name="MigrateAllWebStructures")
    @property
    def migrate_all_web_structures(self) -> Optional[bool]:
        """Gets the MigrateAllWebStructures property"""
        return self.properties.get("MigrateAllWebStructures", None)

    @odata(name="MigrateOneNoteNotebook")
    @property
    def migrate_onenote_notebook(self) -> Optional[bool]:
        """Gets the MigrateOneNoteNotebook property"""
        return self.properties.get("MigrateOneNoteNotebook", None)

    @odata(name="MigrateSchema")
    @property
    def migrate_schema(self) -> Optional[bool]:
        """Gets the MigrateSchema property"""
        return self.properties.get("MigrateSchema", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="PreservePermissionForFileShare")
    @property
    def preserve_permission_for_file_share(self) -> Optional[bool]:
        """Gets the PreservePermissionForFileShare property"""
        return self.properties.get("PreservePermissionForFileShare", None)

    @odata(name="PreserveUserPermissionForOnPrem")
    @property
    def preserve_user_permission_for_on_prem(self) -> Optional[bool]:
        """Gets the PreserveUserPermissionForOnPrem property"""
        return self.properties.get("PreserveUserPermissionForOnPrem", None)

    @odata(name="ReplaceInvalidChars")
    @property
    def replace_invalid_chars(self) -> Optional[bool]:
        """Gets the ReplaceInvalidChars property"""
        return self.properties.get("ReplaceInvalidChars", None)

    @odata(name="ScanOnly")
    @property
    def scan_only(self) -> Optional[bool]:
        """Gets the ScanOnly property"""
        return self.properties.get("ScanOnly", None)

    @odata(name="ScheduledTimeUtc")
    @property
    def scheduled_time_utc(self) -> Optional[datetime]:
        """Gets the ScheduledTimeUtc property"""
        return self.properties.get("ScheduledTimeUtc", datetime.min)

    @odata(name="ScheduledType")
    @property
    def scheduled_type(self) -> Optional[int]:
        """Gets the ScheduledType property"""
        return self.properties.get("ScheduledType", None)

    @odata(name="SettingsUpdateTime")
    @property
    def settings_up_datetime(self) -> Optional[datetime]:
        """Gets the SettingsUpdateTime property"""
        return self.properties.get("SettingsUpdateTime", datetime.min)

    @odata(name="SkipListWithAudienceEnabled")
    @property
    def skip_list_with_audience_enabled(self) -> Optional[bool]:
        """Gets the SkipListWithAudienceEnabled property"""
        return self.properties.get("SkipListWithAudienceEnabled", None)

    @odata(name="SourceListName")
    @property
    def source_list_name(self) -> Optional[str]:
        """Gets the SourceListName property"""
        return self.properties.get("SourceListName", None)

    @odata(name="SourceListRelativePath")
    @property
    def source_list_relative_path(self) -> Optional[str]:
        """Gets the SourceListRelativePath property"""
        return self.properties.get("SourceListRelativePath", None)

    @odata(name="SourceUri")
    @property
    def source_uri(self) -> Optional[str]:
        """Gets the SourceUri property"""
        return self.properties.get("SourceUri", None)

    @odata(name="SourceUserName")
    @property
    def source_user_name(self) -> Optional[str]:
        """Gets the SourceUserName property"""
        return self.properties.get("SourceUserName", None)

    @odata(name="StartMigrationAutomaticallyWhenNoScanIssue")
    @property
    def start_migration_automatically_when_no_scan_issue(self) -> Optional[bool]:
        """Gets the StartMigrationAutomaticallyWhenNoScanIssue property"""
        return self.properties.get("StartMigrationAutomaticallyWhenNoScanIssue", None)

    @odata(name="Tags")
    @property
    def tags(self) -> StringCollection:
        """Gets the Tags property"""
        return self.properties.get("Tags", StringCollection())

    @odata(name="TargetListName")
    @property
    def target_list_name(self) -> Optional[str]:
        """Gets the TargetListName property"""
        return self.properties.get("TargetListName", None)

    @odata(name="TargetListRelativePath")
    @property
    def target_list_relative_path(self) -> Optional[str]:
        """Gets the TargetListRelativePath property"""
        return self.properties.get("TargetListRelativePath", None)

    @odata(name="TargetSiteUrl")
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @odata(name="TargetUserName")
    @property
    def target_user_name(self) -> Optional[str]:
        """Gets the TargetUserName property"""
        return self.properties.get("TargetUserName", None)

    @odata(name="TurnOnDateCreatedFilter")
    @property
    def turn_on_date_created_filter(self) -> Optional[bool]:
        """Gets the TurnOnDateCreatedFilter property"""
        return self.properties.get("TurnOnDateCreatedFilter", None)

    @odata(name="TurnOnDateModifiedFilter")
    @property
    def turn_on_date_modified_filter(self) -> Optional[bool]:
        """Gets the TurnOnDateModifiedFilter property"""
        return self.properties.get("TurnOnDateModifiedFilter", None)

    @odata(name="TurnOnExtensionFilter")
    @property
    def turn_on_extension_filter(self) -> Optional[bool]:
        """Gets the TurnOnExtensionFilter property"""
        return self.properties.get("TurnOnExtensionFilter", None)

    @odata(name="Type")
    @property
    def type(self) -> Optional[int]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    @odata(name="UseCustomAzureStorage")
    @property
    def use_custom_azure_storage(self) -> Optional[bool]:
        """Gets the UseCustomAzureStorage property"""
        return self.properties.get("UseCustomAzureStorage", None)

    @odata(name="UserMappingCSVFile")
    @property
    def user_mapping_csv_file(self) -> Optional[str]:
        """Gets the UserMappingCSVFile property"""
        return self.properties.get("UserMappingCSVFile", None)

    @odata(name="VersionNumsPreserved")
    @property
    def version_nums_preserved(self) -> Optional[int]:
        """Gets the VersionNumsPreserved property"""
        return self.properties.get("VersionNumsPreserved", None)
