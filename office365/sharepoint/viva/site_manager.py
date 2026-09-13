from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.portal.sites.creation_response import SPSiteCreationResponse


class VivaSiteManager(Entity):
    """"""

    def __init__(self, content, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("Microsoft.SharePoint.Portal.VivaSiteManager")
        super().__init__(content, resource_path)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.VivaSiteManager"

    def ensure_viva_site(self) -> ClientResult[SPSiteCreationResponse]:
        """EnsureVivaSite operation."""
        return_type = ClientResult(self.context, SPSiteCreationResponse())
        qry = ServiceOperationQuery(self, "EnsureVivaSite", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
