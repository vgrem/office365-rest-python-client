from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class BaselineSecurityModeThirdPartyAppHPASetting(ClientValue):
    AdditionalApps: StringCollection = field(default_factory=StringCollection)
    Allowlist: StringCollection = field(default_factory=StringCollection)
    Block3PHPA: bool | None = None
    RemovedApps: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.AuthPolicy.BaselineSecurityModeThirdPartyAppHPASetting"
