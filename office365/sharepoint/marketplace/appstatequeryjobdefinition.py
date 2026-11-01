from typing_extensions import Self

from office365.permissions.roles import DirectoryRole
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class SPAppStateQueryJobDefinition(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.SPAppStateQueryJobDefinition"

    @site_access(SiteLevel.FULL_CONTROL, role=DirectoryRole.SharePointAdministrator)
    def perform_fast_revoke_with_client_ids(self) -> Self:
        """PerformFastRevokeWithClientIds operation."""
        qry = ServiceOperationQuery(self, "PerformFastRevokeWithClientIds", None, {}, None, None)
        self.context.add_query(qry)
        return self
