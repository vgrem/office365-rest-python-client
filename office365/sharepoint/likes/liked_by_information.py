from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.likes.user_entity import UserEntity


class LikedByInformation(Entity):
    """Represents the information about the set of users who liked the list item."""

    @property
    def like_count(self) -> Optional[int]:
        """Number of users that have liked the item."""
        return self.properties.get("LikeCount", None)

    @property
    def is_liked_by_user(self) -> Optional[bool]:
        """MUST be TRUE if the current user has liked the list item."""
        return self.properties.get("isLikedByUser", None)

    @odata(name="likedBy")
    @property
    def liked_by(self) -> EntityCollection[UserEntity]:
        """
        List of like entries corresponding to individual likes. MUST NOT contain more than one entry
        for the same user in the set.
        """
        return self.properties.get(
            "likedBy", EntityCollection(self.context, UserEntity, ResourcePath("likedBy", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Likes.LikedByInformation"
