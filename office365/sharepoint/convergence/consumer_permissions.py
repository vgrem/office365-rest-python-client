from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class ConsumerPermissions(Entity):
    def __init__(self, context, path=None):
        if path is None:
            path = ResourcePath("Microsoft.SharePoint.Convergence.ConsumerPermissions")
        super().__init__(context, path)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Convergence.ConsumerPermissions"

    def grant_consumer_site_permissions(self) -> Self:
        """GrantConsumerSitePermissions operation."""
        qry = ServiceOperationQuery(self, "GrantConsumerSitePermissions", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def revoke_consumer_site_permissions(self) -> Self:
        """RevokeConsumerSitePermissions operation."""
        qry = ServiceOperationQuery(self, "RevokeConsumerSitePermissions", None, {}, None, None)
        self.context.add_query(qry)
        return self
