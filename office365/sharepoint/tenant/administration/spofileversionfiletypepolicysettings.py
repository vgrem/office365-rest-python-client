from datetime import time

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SPOFileVersionFileTypePolicySettings(ClientValue):
    def __init__(
        self,
        enable_auto_expiration_version_trim: Optional[bool] = None,
        expire_versions_after: Optional[time] = None,
        extensions: StringCollection = StringCollection(),
        major_version_limit: Optional[int] = None,
        major_with_minor_versions_limit: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self.EnableAutoExpirationVersionTrim = enable_auto_expiration_version_trim
        self.ExpireVersionsAfter = expire_versions_after
        self.Extensions = extensions
        self.MajorVersionLimit = major_version_limit
        self.MajorWithMinorVersionsLimit = major_with_minor_versions_limit
        self.Name = name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionFileTypePolicySettings"
