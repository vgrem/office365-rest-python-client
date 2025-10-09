from office365.runtime.client_value import ClientValue


class SitePermissionsReportDetails(ClientValue):

    def __init__(
        self,
        anyone_links_site_count: int = None,
        eeeu_permission_site_count: int = None,
        report_total_site_count: int = None,
        unique_permission_site_count: int = None,
        unique_site_count: int = None,
    ):
        self.anyoneLinksSiteCount = anyone_links_site_count
        self.eeeuPermissionSiteCount = eeeu_permission_site_count
        self.reportTotalSiteCount = report_total_site_count
        self.uniquePermissionSiteCount = unique_permission_site_count
        self.uniqueSiteCount = unique_site_count

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.SitePermissionsReportDetails"
