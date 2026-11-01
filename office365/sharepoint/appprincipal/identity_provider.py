from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class AppPrincipalIdentityProvider(Entity):
    """Represents an identity provider for app principals."""

    @staticmethod
    @site_access(SiteLevel.READ)
    def external(context) -> "AppPrincipalIdentityProvider":
        return_type = AppPrincipalIdentityProvider(context)
        qry = ServiceOperationQuery(return_type, "External", None, None, None, return_type, True)
        context.add_query(qry)
        return return_type
