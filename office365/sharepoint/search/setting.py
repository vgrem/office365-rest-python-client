from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.search.promoted_results_operations_result import (
    PromotedResultsOperationsResult,
)
from office365.sharepoint.search.query.configuration import QueryConfiguration
from office365.sharepoint.search.reports.base import ReportBase


class SearchSetting(Entity):
    """This object provides the REST operations defined under search settings."""

    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("Microsoft.Office.Server.Search.REST.SearchSetting")
        return self._resource_path

    def get_query_configuration(
        self,
        call_local_search_farms_only: bool = True,
        skip_group_object_id_lookup: Optional[bool] = None,
        throw_on_remote_api_check: Optional[bool] = None,
    ) -> ClientResult[QueryConfiguration]:
        """This operation gets the query configuration from the server. This operation requires that the Search Service
        Application is partitioned. If the Search Service Application is not partitioned the operations returns
        HTTP code 400, not authorized.

        Args:
            call_local_search_farms_only (bool): This is a flag that indicates to only call the local search farm.
            skip_group_object_id_lookup (bool):
            throw_on_remote_api_check (bool):
        """
        return_type = ClientResult(self.context, QueryConfiguration())
        payload = {
            "callLocalSearchFarmsOnly": call_local_search_farms_only,
            "skipGroupObjectIdLookup": skip_group_object_id_lookup,
            "throwOnRemoteApiCheck": throw_on_remote_api_check,
        }
        qry = ServiceOperationQuery(self, "getqueryconfiguration", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def export_search_reports(
        self,
        tenant_id,
        report_type=None,
        interval=None,
        start_date=None,
        end_date=None,
        site_collection_id=None,
    ) -> ClientResult[ReportBase]:
        """Args:
        tenant_id (str):
        report_type (str):
        interval (str):
        start_date (str):
        end_date (str):
        site_collection_id (str):
        """
        return_type = ClientResult(self.context, ReportBase())
        payload = {
            "TenantId": tenant_id,
            "ReportType": report_type,
            "Interval": interval,
            "StartDate": start_date,
            "EndDate": end_date,
            "SiteCollectionId": site_collection_id,
        }
        qry = ServiceOperationQuery(self, "ExportSearchReports", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def ping_admin_endpoint(self) -> ClientResult[bool]:
        """ """
        return_type = ClientResult[bool](self.context)
        qry = ServiceOperationQuery(self, "PingAdminEndpoint", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_promoted_result_query_rules(
        self,
        site_collection_level: Optional[bool] = None,
        offset: Optional[int] = None,
        number_of_rules: Optional[int] = None,
    ) -> ClientResult[PromotedResultsOperationsResult]:
        """The operation is called to retrieve the promoted results (also called Best Bets) for a tenant or a
        site collection.

        Args:
            site_collection_level (bool): This parameter is used by the protocol server to decide which promoted
              results to return to the client. If the parameter is true, the promoted results for the current site
              collection are returned. If the parameter is false, all promoted results for the tenant/Search
              Service Application are returned.
            offset (int): This parameter is the offset into the collection of promoted results. Default value is zero.
              It is used to page through a large result set.
            number_of_rules (int): his parameter is the number of promoted results that are returned in the operation.
              Default value is 100. It is used together with the offset to page through a large result set.
        """
        return_type = ClientResult(self.context, PromotedResultsOperationsResult())
        payload = {
            "siteCollectionLevel": site_collection_level,
            "offset": offset,
            "numberOfRules": number_of_rules,
        }
        qry = ServiceOperationQuery(self, "getpromotedresultqueryrules", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchSetting"
