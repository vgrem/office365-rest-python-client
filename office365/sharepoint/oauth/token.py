from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.oauth.token_response import TokenResponse
from office365.sharepoint.permissions import SiteLevel, site_access


class Token(Entity):
    """"""

    def __init__(self, context):
        super().__init__(context, ResourcePath("SP.OAuth.Token"))

    @site_access(SiteLevel.READ)
    def acquire(self):
        """ """
        return_type = TokenResponse(self.context)
        qry = ServiceOperationQuery(self, "Acquire", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.OAuth.Token"
