from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.tenant.administration.spofileversionfiletypepolicysettings import (
    SPOFileVersionFileTypePolicySettings,
)


class SPOFileVersionPolicySettings(ClientValue):
    def __init__(
        self,
        enable_auto_expiration_version_trim: bool = None,
        expire_versions_after_days: int = None,
        file_types_for_version_expiration: StringCollection = None,
        major_version_limit: int = None,
        major_with_minor_versions_limit: int = None,
        minor_versions_enabled: bool = None,
        versioning_enabled: bool = None,
        version_policy_file_type_override: ClientValueCollection[
            SPOFileVersionFileTypePolicySettings
        ] = ClientValueCollection(SPOFileVersionFileTypePolicySettings),
    ):
        self.EnableAutoExpirationVersionTrim = enable_auto_expiration_version_trim
        self.ExpireVersionsAfterDays = expire_versions_after_days
        self.FileTypesForVersionExpiration = file_types_for_version_expiration
        self.MajorVersionLimit = major_version_limit
        self.MajorWithMinorVersionsLimit = major_with_minor_versions_limit
        self.MinorVersionsEnabled = minor_versions_enabled
        self.VersioningEnabled = versioning_enabled
        self.VersionPolicyFileTypeOverride = version_policy_file_type_override

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionPolicySettings"
