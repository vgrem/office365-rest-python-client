from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.directory.user import User
from office365.sharepoint.entity import Entity


class DirectorySession(Entity):
    def __init__(self, context):
        super().__init__(context, StaticPath("SP.Directory.DirectorySession"))

    @property
    def me(self) -> User:
        return self.properties.get("Me", User(self.context, ResourcePath("Me", self.resource_path)))

    def get_graph_user(self, principal_name: str) -> User:
        """
        :type principal_name: str
        """
        return_type = User(self.context)
        qry = ServiceOperationQuery(self, "GetGraphUser", [principal_name], None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_sharepoint_data_for_user(self, user_id: str) -> User:
        return_type = User(self.context)
        qry = ServiceOperationQuery(self, "GetSharePointDataForUser", [user_id], None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.DirectorySession"
