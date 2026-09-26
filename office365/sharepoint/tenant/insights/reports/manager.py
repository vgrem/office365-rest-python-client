from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.insights.reports.metadata import SPTenantIBInsightsReportMetadata


class SPTenantIBInsightsReportManager(Entity):
    """ """

    def __init__(self, context):
        static_path = StaticPath("Microsoft.SharePoint.Insights.SPTenantIBInsightsReportManager")
        super().__init__(context, static_path)

    def create_report(self) -> SPTenantIBInsightsReportMetadata:
        """"""
        return_type = SPTenantIBInsightsReportMetadata(self.context)
        qry = ServiceOperationQuery(self, "CreateReport", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReportManager"

    def get_report_data(
        self, report_id: UUID, site_type: str, section: str, is_full_details: str
    ) -> ClientResult[StringCollection]:
        """GetReportData operation.

        Args:
            report_id (UUID): reportId parameter
            site_type (str): siteType parameter
            section (str): section parameter
            is_full_details (str): isFullDetails parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetReportData", [report_id, site_type, section, is_full_details], return_type)
        self.context.add_query(qry)
        return return_type
