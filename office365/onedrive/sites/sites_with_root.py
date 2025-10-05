from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.onedrive.internal.paths.root import RootPath
from office365.onedrive.internal.paths.site import SitePath
from office365.onedrive.sites.site import Site
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.read_entity import ReadEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery


class SitesWithRoot(EntityCollection[Site]):
    """Sites container"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Site, resource_path)

    def get_all_sites(self) -> SitesWithRoot:
        """List root sites across geographies in an organization."""
        return_type = SitesWithRoot(self.context)
        qry = FunctionQuery(self, "getAllSites", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_path(self, path: str) -> Site:
        """Address Site resource by server relative path

        :param str path: Server relative path
        """
        tenant_part = self.context.tenant_name.split(".")[0]
        host_name = f"{tenant_part}.sharepoint.com"
        return_type = Site(self.context, SitePath(host_name, path, self.resource_path))
        self.add_child(return_type)
        qry = ReadEntityQuery(return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_url(self, url: str) -> Site:
        """Address Site resource by absolute url

        :param str url: Site absolute url
        """
        return_type = Site(self.context, SitePath.from_url(url, self.resource_path))
        qry = ReadEntityQuery(return_type)
        self.context.add_query(qry)
        return return_type

    def remove(self, sites: SitesWithRoot) -> SitesWithRoot:
        """
        :type sites: SitesWithRoot
        """
        return_type = SitesWithRoot(self.context, self.resource_path)
        payload = {
            "value": sites,
        }
        qry = ServiceOperationQuery(self, "remove", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def search(self, query_text: str) -> SitesWithRoot:
        """
        Search across a SharePoint tenant for sites that match keywords provided.

        The only property that works for sorting is createdDateTime. The search filter is a free text search that uses
        multiple properties when retrieving the search results.

        :param str query_text: str
        """
        return_type = SitesWithRoot(self.context, ResourcePath("sites"))
        return_type.query_options.custom["search"] = query_text
        self.context.load(return_type)
        return return_type

    @property
    def root(self) -> Site:
        return self.properties.get(
            "root", Site(self.context, RootPath(self.resource_path, self.resource_path))
        )
