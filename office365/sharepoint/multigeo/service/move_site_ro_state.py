from __future__ import annotations

from typing_extensions import Self

from office365.permissions.roles import DirectoryRole
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class MoveSiteROState(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.MoveSiteROState"

    @site_access(SiteLevel.FULL_CONTROL, role=DirectoryRole.SharePointAdministrator)
    def update_site_ro_state(self) -> Self:
        """UpdateSiteROState operation."""
        qry = ServiceOperationQuery(self, "UpdateSiteROState", None, {}, None, None)
        self.context.add_query(qry)
        return self
