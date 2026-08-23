from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.rcd_site_status_detail import RcdSiteStatusDetail


class RcdCategoryDetailResult(ClientValue):
    sites: ClientValueCollection[RcdSiteStatusDetail] = field(
        default_factory=lambda: ClientValueCollection(RcdSiteStatusDetail)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.RcdCategoryDetailResult"
