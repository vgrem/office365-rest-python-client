from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.list_of_ids_provider_parameters import ListOfIdsProviderParameters
from office365.sharepoint.sites.manager.top_site_pages_provider_parameters import TopSitePagesProviderParameters


class BAAAItemProviderRequest(ClientValue):
    ItemProviderType: int | None = None
    ListOfIds: ListOfIdsProviderParameters = field(default_factory=ListOfIdsProviderParameters)
    TopSitePages: TopSitePagesProviderParameters = field(default_factory=TopSitePagesProviderParameters)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BAAAItemProviderRequest"
