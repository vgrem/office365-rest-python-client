from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SPOFileVersionFileTypePolicySettings(ClientValue):
    EnableAutoExpirationVersionTrim: bool | None = None
    ExpireVersionsAfter: time | None = None
    Extensions: StringCollection = field(default_factory=lambda: StringCollection())
    MajorVersionLimit: int | None = None
    MajorWithMinorVersionsLimit: int | None = None
    Name: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionFileTypePolicySettings"
