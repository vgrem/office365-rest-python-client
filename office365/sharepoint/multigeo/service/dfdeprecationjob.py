from typing_extensions import Self

from office365.permissions.roles import DirectoryRole
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class DfDeprecationJob(Entity):
    @site_access(SiteLevel.WRITE, role=DirectoryRole.SharePointAdministrator)
    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete", None, {}, None, None)
        self.context.add_query(qry)
        return self
