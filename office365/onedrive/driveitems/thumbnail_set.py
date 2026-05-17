from office365.entity import Entity
from office365.onedrive.driveitems.thumbnail import Thumbnail


class ThumbnailSet(Entity):
    """The ThumbnailSet resource is a keyed collection of thumbnail resources.
    It is used to represent a set of thumbnails associated with a DriveItem."""

    @property
    def large(self) -> Thumbnail:
        """A 1920x1920 scaled thumbnail."""
        return self.properties.get("large", Thumbnail())

    @property
    def medium(self) -> Thumbnail:
        """A 176x176 scaled thumbnail."""
        return self.properties.get("medium", Thumbnail())

    @property
    def small(self) -> Thumbnail:
        """A 48x48 cropped thumbnail."""
        return self.properties.get("small", Thumbnail())

    @property
    def source(self) -> Thumbnail:
        """A custom thumbnail image or the original image used to generate other thumbnails."""
        return self.properties.get("source", Thumbnail())
