from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.tenant.administration.spofileversionfiletypepolicysettings import (
    SPOFileVersionFileTypePolicySettings,
)


@dataclass
class SPOFileVersionPolicySettings(ClientValue):
    EnableAutoExpirationVersionTrim: bool | None = None
    ExpireVersionsAfterDays: int | None = None
    FileTypesForVersionExpiration: StringCollection | None = None
    MajorVersionLimit: int | None = None
    MajorWithMinorVersionsLimit: int | None = None
    MinorVersionsEnabled: bool | None = None
    VersioningEnabled: bool | None = None
    VersionPolicyFileTypeOverride: ClientValueCollection[SPOFileVersionFileTypePolicySettings] = field(
        default_factory=lambda: ClientValueCollection(SPOFileVersionFileTypePolicySettings)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionPolicySettings"
