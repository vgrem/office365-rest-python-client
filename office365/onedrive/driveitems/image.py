from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Image(ClientValue):
    """
    The Image resource groups image-related properties into a single structure. If a DriveItem has a
    non-null image facet, the item represents a bitmap image.

    Note: If the service is unable to determine the width and height of the image, the Image resource may be empty.
    """

    height: int | None = None
    width: int | None = None
