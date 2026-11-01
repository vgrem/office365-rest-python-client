from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access
from office365.sharepoint.portal.linkedsites.list_contract import LinkedSitesListContract


class SiteLinkingManager(Entity):
    """"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, resource_path)

    @site_access(SiteLevel.READ)
    def get_site_links(self):
        """ """
        result = ClientResult(self.context, LinkedSitesListContract())
        qry = ServiceOperationQuery(self, "GetSiteLinks", None, None, None, result)
        self.context.add_query(qry)
        return result

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SiteLinkingManager"

    @site_access(SiteLevel.WRITE)
    def link_group(self, group_id: UUID) -> ClientResult[bool]:
        """LinkGroup operation.

        Args:
            group_id (UUID): groupId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "LinkGroup", None, {"groupId": group_id}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @site_access(SiteLevel.WRITE)
    def unlink_group(self, group_id: UUID) -> ClientResult[bool]:
        """UnlinkGroup operation.

        Args:
            group_id (UUID): groupId parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "UnlinkGroup", None, {"groupId": group_id}, None, return_type)
        self.context.add_query(qry)
        return return_type
