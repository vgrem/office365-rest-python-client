from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MigrationTaskSettings(ClientValue):
    AgentGroupName: Optional[str] = None
    AzureActiveDirectoryLkp: Optional[bool] = None
    CustomAzureAccessKey: Optional[str] = None
    CustomAzureDeletionAfterMig: Optional[bool] = None
    CustomAzureStorageAccount: Optional[str] = None
    DateCreated: Optional[datetime] = None
    DateModified: Optional[datetime] = None
    DeltaSyncDateTimeFilter: Optional[datetime] = None
    DeltaSyncEnabled: Optional[bool] = None
    EnableIncremental: Optional[bool] = None
    EnableUserMappings: Optional[bool] = None
    Encrypted: Optional[bool] = None
    FilterOutHiddenFiles: Optional[bool] = None
    FilterOutPathSpecialCharacters: Optional[bool] = None
    IgnoredFileExtensions: Optional[str] = None
    InvalidCharsReplacement: Optional[str] = None
    MigrateAllWebStructures: Optional[bool] = None
    MigrateOneNoteNotebook: Optional[bool] = None
    MigrateSchema: Optional[bool] = None
    PreservePermissionForFileShare: Optional[bool] = None
    PreserveUserPermissionForOnPrem: Optional[bool] = None
    ReplaceInvalidChars: Optional[bool] = None
    ScanOnly: Optional[bool] = None
    SettingsUpdateTime: Optional[datetime] = None
    SkipListWithAudienceEnabled: Optional[bool] = None
    StartMigrationAutomaticallyWhenNoScanIssue: Optional[bool] = None
    Tags: Optional[StringCollection] = None
    TurnOnDateCreatedFilter: Optional[bool] = None
    TurnOnDateModifiedFilter: Optional[bool] = None
    TurnOnExtensionFilter: Optional[bool] = None
    UseCustomAzureStorage: Optional[bool] = None
    UserMappingCSVFile: Optional[str] = None
    VersionNumsPreserved: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskSettings"
