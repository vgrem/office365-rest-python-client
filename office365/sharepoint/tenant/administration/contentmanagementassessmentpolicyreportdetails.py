from office365.runtime.client_value import ClientValue


class ContentManagementAssessmentPolicyReportDetails(ClientValue):

    def __init__(
        self,
        total_impacted_sites: int = None,
        total_inactive_sites: int = None,
        total_ownerless_sites: int = None,
    ):
        self.totalImpactedSites = total_impacted_sites
        self.totalInactiveSites = total_inactive_sites
        self.totalOwnerlessSites = total_ownerless_sites

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentPolicyReportDetails"
