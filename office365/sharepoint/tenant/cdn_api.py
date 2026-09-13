from __future__ import annotations

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.cdn_url import TenantCdnUrl


class TenantCdnApi(Entity):
    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("Microsoft.SharePoint.TenantCdn.TenantCdnApi")
        return self._resource_path

    def get_cdn_urls(self, items=None):
        """Args:
        items (list[str]):
        """
        payload = {"items": items}
        return_type = ClientResult(self.context, ClientValueCollection(TenantCdnUrl))
        qry = ServiceOperationQuery(self, "GetCdnUrls", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.TenantCdn.TenantCdnApi"

    def is_folder_urls_in_tenant_cdn(self, urls: list[str], cdn_type: int) -> ClientResult[ClientValueCollection[bool]]:
        """IsFolderUrlsInTenantCdn operation.

        Args:
            urls (list[str]): urls parameter
            cdn_type (int): cdnType parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection(bool))
        qry = FunctionQuery(self, "IsFolderUrlsInTenantCdn", [StringCollection(urls), cdn_type], return_type)
        self.context.add_query(qry)
        return return_type
