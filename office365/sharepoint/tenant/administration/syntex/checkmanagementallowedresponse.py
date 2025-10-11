from office365.runtime.client_value import ClientValue


class SyntexCheckManagementAllowedResponse(ClientValue):

    def __init__(self, allowed_billing_only: bool = None, allowed_license_or_billing: bool = None):
        self.allowedBillingOnly = allowed_billing_only
        self.allowedLicenseOrBilling = allowed_license_or_billing

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexCheckManagementAllowedResponse"
