from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.viva.app_configuration import AppConfiguration
from office365.sharepoint.viva.connections.page import VivaConnectionsPage
from office365.sharepoint.viva.dashboard.configuration import DashboardConfiguration
from office365.sharepoint.viva.home import VivaHome


class EmployeeEngagement(Entity):
    """ """

    def __init__(self, context):
        super().__init__(context, ResourcePath("SP.EmployeeEngagement"))

    def dashboard_content(self, override_language_code: Optional[str] = None) -> ClientResult[str]:
        """Args:
        override_language_code (str):
        """
        return_type = ClientResult(self.context, str())
        payload = {"override_language_code": override_language_code}
        qry = ServiceOperationQuery(self, "DashboardContent", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def full_dashboard_content(
        self, canvas_as_json: Optional[bool] = None, include_personalization_data: Optional[bool] = None
    ) -> ClientResult[DashboardConfiguration]:
        """Args:
        canvas_as_json (bool):
        include_personalization_data (bool):
        """
        return_type = ClientResult(self.context, DashboardConfiguration())
        payload = {
            "canvasAsJson": canvas_as_json,
            "includePersonalizationData": include_personalization_data,
        }
        qry = ServiceOperationQuery(self, "FullDashboardContent", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def viva_home_configuration(self):
        return_type = ClientResult(self.context, {})
        qry = FunctionQuery(self, "VivaHomeConfiguration", None, return_type)
        self.context.add_query(qry)
        return return_type

    def viva_home(self) -> VivaHome:
        return_type = VivaHome(self.context)
        qry = ServiceOperationQuery(self, "VivaHome", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="AppConfiguration")
    @property
    def app_configuration(self) -> AppConfiguration:
        return self.properties.get(
            "AppConfiguration",
            AppConfiguration(self.context, ResourcePath("AppConfiguration", self.resource_path)),
        )

    @odata(name="VivaConnectionsPage")
    @property
    def viva_connections_page(self) -> VivaConnectionsPage:
        return self.properties.get(
            "VivaConnectionsPage",
            VivaConnectionsPage(self.context, ResourcePath("VivaConnectionsPage", self.resource_path)),
        )
