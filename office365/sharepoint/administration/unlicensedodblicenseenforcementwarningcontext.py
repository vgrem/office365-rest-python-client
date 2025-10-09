from datetime import datetime

from office365.runtime.client_value import ClientValue


class UnlicensedOdbLicenseEnforcementWarningContext(ClientValue):

    def __init__(
        self,
        generated_on: datetime = None,
        warning_status: int = None,
        warning_status_effective_until: datetime = None,
    ):
        self.GeneratedOn = generated_on
        self.WarningStatus = warning_status
        self.WarningStatusEffectiveUntil = warning_status_effective_until

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.UnlicensedOdbLicenseEnforcementWarningContext"
