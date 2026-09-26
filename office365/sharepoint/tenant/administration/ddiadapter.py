from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class DDIAdapter(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdmin.MiddleTier.DDIAdapter"

    def get_list(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """GetList operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "GetList", None, {"schema": schema, "workflow": workflow, "stream": stream}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_object(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """GetObject operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "GetObject", None, {"schema": schema, "workflow": workflow, "stream": stream}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def multi_object_execute(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """MultiObjectExecute operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "MultiObjectExecute",
            None,
            {"schema": schema, "workflow": workflow, "stream": stream},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def new_object(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """NewObject operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "NewObject", None, {"schema": schema, "workflow": workflow, "stream": stream}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def remove_objects(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """RemoveObjects operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "RemoveObjects", None, {"schema": schema, "workflow": workflow, "stream": stream}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def set_object(self, schema: str, workflow: str, stream: bytes) -> ClientResult[str]:
        """SetObject operation.

        Args:
            schema (str): schema parameter
            workflow (str): workflow parameter
            stream (bytes): stream parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "SetObject", None, {"schema": schema, "workflow": workflow, "stream": stream}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
