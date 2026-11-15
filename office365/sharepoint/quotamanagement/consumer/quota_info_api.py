from __future__ import annotations

from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class ConsumerQuotaInfoApi(Entity):
    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def get_quota_info(self) -> ClientResult[str]:
        """GetQuotaInfo operation."""
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "GetQuotaInfo", [], return_type)
        self.context.add_query(qry)
        return return_type
