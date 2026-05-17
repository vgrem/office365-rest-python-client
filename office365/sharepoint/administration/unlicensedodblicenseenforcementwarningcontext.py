from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class UnlicensedOdbLicenseEnforcementWarningContext(ClientValue):
    def __init__(
        self,
        generated_on: Optional[datetime] = None,
        warning_status: Optional[int] = None,
        warning_status_effective_until: Optional[datetime] = None,
    ):
        self.GeneratedOn = generated_on
        self.WarningStatus = warning_status
        self.WarningStatusEffectiveUntil = warning_status_effective_until

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.UnlicensedOdbLicenseEnforcementWarningContext"
