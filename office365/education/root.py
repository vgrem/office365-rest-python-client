from office365.education.classes.type import EducationClass
from office365.education.users.user import EducationUser
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class EducationRoot(Entity):
    """The /education namespace exposes functionality that is specific to the education sector."""

    @property
    def classes(self) -> EntityCollection[EducationClass]:
        return self.properties.get(
            "classes",
            EntityCollection(
                self.context,
                EducationClass,
                ResourcePath("classes", self.resource_path),
            ),
        )

    @property
    def me(self) -> EducationUser:
        return self.properties.get("me", EducationUser(self.context, ResourcePath("me", self.resource_path)))

    @property
    def users(self) -> EntityCollection[EducationUser]:
        return self.properties.get(
            "users",
            EntityCollection(self.context, EducationUser, ResourcePath("users", self.resource_path)),
        )
