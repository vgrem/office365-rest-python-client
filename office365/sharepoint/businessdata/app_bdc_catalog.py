from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class AppBdcCatalog(Entity):
    """
    Represents the Business Data Connectivity (BDC) MetadataCatalog for an application that contains external content
    types provisioned by the application.
    """

    def get_permissible_connections(self) -> ClientResult[StringCollection]:
        """
        Gets the list of external connections that the application has permissions to use.
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = ServiceOperationQuery(self, "GetPermissibleConnections", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.BusinessData.AppBdcCatalog"

    def get_connection_id(self, lob_system_name: str, lob_system_instance_name: str) -> ClientResult[str]:
        """GetConnectionId operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            lob_system_instance_name (str): lobSystemInstanceName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "GetConnectionId",
            None,
            {"lobSystemName": lob_system_name, "lobSystemInstanceName": lob_system_instance_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_lob_system_instance_property(
        self, lob_system_name: str, lob_system_instance_name: str, property_name: str
    ) -> ClientResult[str]:
        """GetLobSystemInstanceProperty operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            lob_system_instance_name (str): lobSystemInstanceName parameter
            property_name (str): propertyName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "GetLobSystemInstanceProperty",
            None,
            {
                "lobSystemName": lob_system_name,
                "lobSystemInstanceName": lob_system_instance_name,
                "propertyName": property_name,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_lob_system_property(self, lob_system_name: str, property_name: str) -> ClientResult[str]:
        """GetLobSystemProperty operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            property_name (str): propertyName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "GetLobSystemProperty",
            None,
            {"lobSystemName": lob_system_name, "propertyName": property_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def set_connection_id(self, lob_system_name: str, lob_system_instance_name: str, connection_id: str) -> Self:
        """SetConnectionId operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            lob_system_instance_name (str): lobSystemInstanceName parameter
            connection_id (str): connectionId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SetConnectionId",
            None,
            {
                "lobSystemName": lob_system_name,
                "lobSystemInstanceName": lob_system_instance_name,
                "connectionId": connection_id,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def set_lob_system_instance_property(
        self, lob_system_name: str, lob_system_instance_name: str, property_name: str, property_value: str
    ) -> Self:
        """SetLobSystemInstanceProperty operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            lob_system_instance_name (str): lobSystemInstanceName parameter
            property_name (str): propertyName parameter
            property_value (str): propertyValue parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SetLobSystemInstanceProperty",
            None,
            {
                "lobSystemName": lob_system_name,
                "lobSystemInstanceName": lob_system_instance_name,
                "propertyName": property_name,
                "propertyValue": property_value,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def set_lob_system_property(self, lob_system_name: str, property_name: str, property_value: str) -> Self:
        """SetLobSystemProperty operation.

        Args:
            lob_system_name (str): lobSystemName parameter
            property_name (str): propertyName parameter
            property_value (str): propertyValue parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SetLobSystemProperty",
            None,
            {"lobSystemName": lob_system_name, "propertyName": property_name, "propertyValue": property_value},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
