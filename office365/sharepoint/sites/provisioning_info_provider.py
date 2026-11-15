from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class SiteProvisioningInfoProvider(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Client.Search.Administration.SiteProvisioningInfoProvider"

    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def check_site_ingestion_status(self, site_id: str) -> ClientResult[bool]:
        """CheckSiteIngestionStatus operation.

        Args:
            site_id (str): siteId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "CheckSiteIngestionStatus", [site_id], return_type)
        self.context.add_query(qry)
        return return_type
