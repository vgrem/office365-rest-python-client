from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.files.file import File
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

    @property
    def bannerimages(self) -> EntityCollection[File]:
        """Gets the bannerimages property"""
        return self.properties.get(
            "bannerimages", EntityCollection[File](self.context, File, ResourcePath("bannerimages", self.resource_path))
        )

    def add_banner_image_from_url(self, from_image_url: str) -> ClientResult[str]:
        """AddBannerImageFromUrl operation.

        Args:
            from_image_url (str): fromImageUrl parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "AddBannerImageFromUrl", None, {"fromImageUrl": from_image_url}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def delete_magazine(self) -> Self:
        """DeleteMagazine operation."""
        qry = ServiceOperationQuery(self, "DeleteMagazine", None, {}, None, None)
        self.context.add_query(qry)
        return self
