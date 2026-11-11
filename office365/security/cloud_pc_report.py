from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection

if TYPE_CHECKING:
    from office365.intune.devices.management.virtualendpoint.cloudpcs.cloud_pc_recommendation_report_type import (
        CloudPcRecommendationReportType,
    )


class CloudPcReport(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcReport"

    @require_permission(delegated=["CloudPC.ReadWrite.All"], application=["CloudPC.ReadWrite.All"])
    def retrieve_cloud_pc_recommendation_reports(
        self,
        report_type: CloudPcRecommendationReportType,
        filter_: str,
        select: list[str],
        search: str,
        group_by: list[str],
        order_by: list[str],
        skip: int,
        top: int,
    ) -> ClientResult[bytes]:
        """retrieveCloudPcRecommendationReports operation.

        Args:
            report_type (CloudPcRecommendationReportType):
                reportType parameter
            filter_ (str):
                filter parameter
            select (list[str]):
                select parameter
            search (str):
                search parameter
            group_by (list[str]):
                groupBy parameter
            order_by (list[str]):
                orderBy parameter
            skip (int):
                skip parameter
            top (int):
                top parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self,
            "retrieveCloudPcRecommendationReports",
            None,
            {
                "reportType": report_type,
                "filter": filter_,
                "select": StringCollection(select),
                "search": search,
                "groupBy": StringCollection(group_by),
                "orderBy": StringCollection(order_by),
                "skip": skip,
                "top": top,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
