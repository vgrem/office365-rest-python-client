from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.principal.users.user import User


class VideoPermissionGroup(Entity):
    @odata(name="Users", navigation=True)
    @property
    def users(self) -> EntityCollection[User]:
        """Gets the Users property"""
        return self.properties.get(
            "Users", EntityCollection[User](self.context, User, ResourcePath("Users", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoPermissionGroup"

    @odata(name="Id")
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    def has_current_user(self) -> ClientResult[bool]:
        """HasCurrentUser operation."""
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "HasCurrentUser", [], return_type)
        self.context.add_query(qry)
        return return_type
