from __future__ import annotations

from typing import TYPE_CHECKING

from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class AppCatalog(Entity):
    @staticmethod
    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def is_app_sideloading_enabled(context: ClientContext) -> ClientResult[bool]:
        """IsAppSideloadingEnabled operation."""
        from office365.sharepoint.apps.catalog import AppCatalog

        return_type = ClientResult(context, bool())
        qry = ServiceOperationQuery(AppCatalog(context), "IsAppSideloadingEnabled", None, {}, None, return_type, True)
        context.add_query(qry)
        return return_type
