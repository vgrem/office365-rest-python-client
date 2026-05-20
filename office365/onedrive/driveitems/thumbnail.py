from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Thumbnail(ClientValue):
    """
    The thumbnail resource type represents a thumbnail for an image, video, document,
        or any item that has a bitmap representation.
    """

    content: str | None = None
    height: int | None = None
    sourceItemId: str | None = None
    url: str | None = None
    width: int | None = None
