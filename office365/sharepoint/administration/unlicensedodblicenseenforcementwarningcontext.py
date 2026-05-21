from __future__ import annotations

from datetime import datetime
from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class UnlicensedOdbLicenseEnforcementWarningContext(ClientValue):

    GeneratedOn: Optional[datetime] = None
    WarningStatus: Optional[int] = None
    WarningStatusEffectiveUntil: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.UnlicensedOdbLicenseEnforcementWarningContext"