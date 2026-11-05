from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.topsitefile import TopSiteFile


class TopSiteFilesResult(ClientValue):
    Files: ClientValueCollection[TopSiteFile] = field(default_factory=lambda: ClientValueCollection(TopSiteFile))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.TopSiteFilesResult"
