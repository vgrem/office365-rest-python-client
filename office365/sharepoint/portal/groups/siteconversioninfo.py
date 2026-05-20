from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class GroupSiteConversionInfo(ClientValue):
    GroupType: Optional[int] = None
    IsGroupifyDisabled: Optional[bool] = None
    IsRegionRestricted: Optional[bool] = None
    IsWrongPdl: Optional[bool] = None
    SuggestedMembers: StringCollection = field(default_factory=StringCollection)
    SuggestedOwners: StringCollection = field(default_factory=StringCollection)
    UnsuggestablePrincipals: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupSiteConversionInfo"
