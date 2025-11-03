from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.principal.users.user import User


class VideoPermissionGroup(Entity):

    @property
    def users(self) -> EntityCollection[User]:
        """Gets the Users property"""
        return self.properties.get(
            "Users", EntityCollection[User](self.context, User, ResourcePath("Users", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoPermissionGroup"
