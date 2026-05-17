from typing import Any

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.likes.user_entity import UserEntity


class Comment(Entity):
    def like(self) -> Self:
        """
        The Like method makes the current user a liker of the comment.
        """
        qry = ServiceOperationQuery(self, "Like")
        self.context.add_query(qry)
        return self

    def unlike(self) -> Self:
        """
        The Unlike method removes the current user from the list of likers for the comment.
        """
        qry = ServiceOperationQuery(self, "Unlike")
        self.context.add_query(qry)
        return self

    @property
    def liked_by(self) -> EntityCollection[UserEntity]:
        """
        List of like entries corresponding to individual likes. MUST NOT contain more than one entry
        for the same user in the set.
        """
        return self.properties.get(
            "likedBy",
            EntityCollection(self.context, UserEntity, ResourcePath("likedBy", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Comments.comment"

    def get_property(self, name: str, default_value: Any = None):
        if default_value is None:
            property_mapping = {
                "likedBy": self.liked_by,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
