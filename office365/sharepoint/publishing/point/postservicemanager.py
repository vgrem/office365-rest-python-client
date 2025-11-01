from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.publishing.point.magazineprops import PointPublishingMagazineProps
from office365.sharepoint.publishing.point.post import PointPublishingPost
from office365.sharepoint.publishing.point.user import PointPublishingUser


class PointPublishingPostServiceManager(Entity):

    @property
    def contributors(self) -> EntityCollection[PointPublishingUser]:
        """Gets the contributors property"""
        return self.properties.get(
            "contributors",
            EntityCollection[PointPublishingUser](
                self.context, PointPublishingUser, ResourcePath("contributors", self.resource_path)
            ),
        )

    @property
    def creators(self) -> EntityCollection[PointPublishingUser]:
        """Gets the creators property"""
        return self.properties.get(
            "creators",
            EntityCollection[PointPublishingUser](
                self.context, PointPublishingUser, ResourcePath("creators", self.resource_path)
            ),
        )

    @property
    def magazineprops(self) -> PointPublishingMagazineProps:
        """Gets the magazineprops property"""
        return self.properties.get(
            "magazineprops",
            PointPublishingMagazineProps(self.context, ResourcePath("magazineprops", self.resource_path)),
        )

    @property
    def posts(self) -> EntityCollection[PointPublishingPost]:
        """Gets the posts property"""
        return self.properties.get(
            "posts",
            EntityCollection[PointPublishingPost](
                self.context, PointPublishingPost, ResourcePath("posts", self.resource_path)
            ),
        )

    @property
    def viewers(self) -> EntityCollection[PointPublishingUser]:
        """Gets the viewers property"""
        return self.properties.get(
            "viewers",
            EntityCollection[PointPublishingUser](
                self.context, PointPublishingUser, ResourcePath("viewers", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingPostServiceManager"
