from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SiteAdministratorsFieldsData(ClientValue):
    def __init__(
        self,
        site_administrators: StringCollection = StringCollection(),
        site_id: Optional[UUID] = None,
    ):
        self.siteAdministrators = site_administrators
        self.siteId = site_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsFieldsData"
