from office365.runtime.client_result import ClientResult
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.clientsidecomponent.hostedapps.app import HostedApp
from office365.sharepoint.entity import Entity


class HostedAppsManager(Entity):
    """Hosted Apps Manager"""

    def get_by_id(self, id_: str) -> HostedApp:
        """Gets an hosted app based on the Id.

        Args:
            id_ (str): The Id of the hosted app to get.
        """
        return HostedApp(self.context, ServiceOperationPath("GetById", [id_], self.resource_path))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.HostedAppsManager"

    def add(self, web_part_data_as_json: str, host_type: str) -> ClientResult[int]:
        """Add operation.

        Args:
            web_part_data_as_json (str): webPartDataAsJson parameter
            host_type (str): hostType parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(
            self, "Add", None, {"webPartDataAsJson": web_part_data_as_json, "hostType": host_type}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
