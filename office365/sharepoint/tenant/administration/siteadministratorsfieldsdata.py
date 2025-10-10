from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SiteAdministratorsFieldsData(ClientValue):

    def __init__(
        self,
        site_administrators: StringCollection = StringCollection(),
        site_id: UUID = None,
    ):
        self.siteAdministrators = site_administrators
        self.siteId = site_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsFieldsData"
