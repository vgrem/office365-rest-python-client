from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity


class MigrationSPFlight(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationSPFlight"

    def is_flight_enabled(self, flight_name: str) -> ClientResult[bool]:
        """IsFlightEnabled operation.

        Args:
            flight_name (str): flightName parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "IsFlightEnabled", [flight_name], return_type)
        self.context.add_query(qry)
        return return_type
