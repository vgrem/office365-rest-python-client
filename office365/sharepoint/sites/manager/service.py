from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.sites.manager.topsitefilesresult import TopSiteFilesResult


class SiteManagerService(Entity):
    """ """

    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("Microsoft.SharePoint.SiteManager.SiteManagerService")
        return self._resource_path

    def top_files(self, max_count: Optional[int] = None) -> ClientResult[TopSiteFilesResult]:
        """ """
        return_type = ClientResult(self.context, TopSiteFilesResult())
        payload = {"maxCount": max_count}
        qry = ServiceOperationQuery(
            self,
            "TopFiles",
            None,
            payload,
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SiteManagerService"
