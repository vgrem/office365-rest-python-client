from datetime import time

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPOFileVersionFileTypePolicySettings(ClientValue):
    def __init__(
        self,
        enable_auto_expiration_version_trim: bool = None,
        expire_versions_after: time = None,
        extensions: StringCollection = StringCollection(),
        major_version_limit: int = None,
        major_with_minor_versions_limit: int = None,
        name: str = None,
    ):
        self.EnableAutoExpirationVersionTrim = enable_auto_expiration_version_trim
        self.ExpireVersionsAfter = expire_versions_after
        self.Extensions = extensions
        self.MajorVersionLimit = major_version_limit
        self.MajorWithMinorVersionsLimit = major_with_minor_versions_limit
        self.Name = name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionFileTypePolicySettings"
