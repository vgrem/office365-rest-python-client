from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access
from office365.sharepoint.viva.connections.configurationanddata import ConnectionsConfigurationAndData
from office365.sharepoint.viva.spotlightconfiguration import SpotlightConfiguration


class VivaConnectionsPage(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.VivaConnectionsPage"

    @site_access(SiteLevel.READ)
    def get_data(self) -> ClientResult[ConnectionsConfigurationAndData]:
        """GetData operation."""
        return_type = ClientResult(self.context, ConnectionsConfigurationAndData())
        qry = FunctionQuery(self, "GetData", [], return_type)
        self.context.add_query(qry)
        return return_type

    @site_access(SiteLevel.WRITE)
    def set_spotlight_configuration(
        self, configuration: SpotlightConfiguration
    ) -> ClientResult[ConnectionsConfigurationAndData]:
        """SetSpotlightConfiguration operation.

        Args:
            configuration (SpotlightConfiguration): configuration parameter
        """
        return_type = ClientResult(self.context, ConnectionsConfigurationAndData())
        qry = ServiceOperationQuery(
            self, "SetSpotlightConfiguration", None, {"configuration": configuration}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
