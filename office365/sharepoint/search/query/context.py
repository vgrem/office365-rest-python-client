from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class QueryContext(ClientValue):
    """This object contains the query context properties."""

    def __init__(
        self,
        group_object_ids=None,
        site_id=None,
        tenant_instance_id=None,
        portal_url: str = None,
        role_ids: GuidCollection = GuidCollection(),
        sp_site_id: str = None,
        sp_web_id: str = None,
    ):
        """
        :param str site_id: This property contains the site identification.
        """
        self.GroupObjectIds = StringCollection(group_object_ids)
        self.SpSiteId = site_id
        self.TenantInstanceId = tenant_instance_id
        self.PortalUrl = portal_url
        self.RoleIds = role_ids
        self.SpSiteId = sp_site_id
        self.SpWebId = sp_web_id

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryContext"
