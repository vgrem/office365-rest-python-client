from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Image(ClientValue):
    """
    The Image resource groups image-related properties into a single structure. If a DriveItem has a
    non-null image facet, the item represents a bitmap image.

    Note: If the service is unable to determine the width and height of the image, the Image resource may be empty.
    """

    height: int | None = None
    width: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Image"
