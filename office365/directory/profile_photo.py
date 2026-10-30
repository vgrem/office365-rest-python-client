from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ProfilePhoto(Entity):
    """
    A profile photo of a user, group or an Outlook contact accessed from Exchange Online.
    It's binary data not encoded in base-64.

    The supported sizes of HD photos on Exchange Online are as follows: '48x48', '64x64', '96x96', '120x120',
    '240x240', '360x360','432x432', '504x504', and '648x648'.
    """

    @odata(name="height")
    @property
    def height(self) -> Optional[int]:
        """The height of the photo."""
        return self.properties.get("height", None)

    @odata(name="width")
    @property
    def width(self) -> Optional[int]:
        """The width of the photo."""
        return self.properties.get("width", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProfilePhoto"
