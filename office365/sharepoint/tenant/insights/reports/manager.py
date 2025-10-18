from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.insights.reports.metadata import (
    SPTenantIBInsightsReportMetadata,
)


class SPTenantIBInsightsReportManager(Entity):
    """ """

    def __init__(self, context):
        static_path = StaticPath("Microsoft.SharePoint.Insights.SPTenantIBInsightsReportManager")
        super().__init__(context, static_path)

    def create_report(self) -> SPTenantIBInsightsReportMetadata:
        """"""
        return_type = SPTenantIBInsightsReportMetadata(self.context)
        qry = ServiceOperationQuery(
            self,
            "CreateReport",
            None,
            None,
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReportManager"
