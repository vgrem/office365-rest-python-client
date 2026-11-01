from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class TeamsPackageDownload(Entity):
    """"""

    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def download_teams(self) -> ClientResult[bytes]:
        """ """
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "DownloadTeams", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.TeamsPackageDownload"
